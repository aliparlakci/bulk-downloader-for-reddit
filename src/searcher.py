import argparse
import os
import sys
from pathlib import Path
from time import localtime, strftime

try:
    import praw
except ModuleNotFoundError:
    print("\nPRAW not found on your computer, installing...\n")
    from src.tools import install
    install("praw")
    import praw

from prawcore.exceptions import NotFound

from src.tools import GLOBAL, createLogFile, jsonFile, printToFile
from src.errors import (NoMatchingSubmissionFound, NoPrawSupport,
                        NoRedditSupoort, MultiredditNotFound,
                        InvalidSortingType)

print = printToFile

def beginPraw(config,user_agent = "newApp",TwoFA=False):
    """Start reddit instance"""
    if not TwoFA:
        return praw.Reddit(client_id = config['reddit_client_id'],
                           client_secret = (config['reddit_client_secret']),
                           password = config['reddit_password'],
                           user_agent = user_agent,
                           username = config['reddit_username'])
    else:
        return praw.Reddit(client_id = config['reddit_client_id'],
                           client_secret = (config['reddit_client_secret']),
                           password = (
                               config['reddit_password']
                               + ":"
                               + TwoFA
                           ),
                           user_agent = user_agent,
                           username = config['reddit_username'])

def getPosts(args):
    """Call PRAW regarding to arguments and pass it to redditSearcher.
    Return what redditSearcher has returned.
    """

    config = GLOBAL.config
    if GLOBAL.arguments.auth is not None:
        reddit = beginPraw(config,GLOBAL.arguments.auth)
    else:
        reddit = beginPraw(config)

    if args["sort"] == "best":
        raise NoPrawSupport

    print("\nSEARCHING STARTED\n")

    try:
        if args["sort"] == "top" or args["sort"] == "controversial":
            keyword_params = {
                "time_filter":args["time"],
                "limit":args["limit"]
            }
        # OTHER SORT TYPES DON'T TAKE TIME_FILTER
        else:
            keyword_params = {
                "limit":args["limit"]
            }
    except KeyError:
        pass

    if "search" in args:
        if args["sort"] in ["rising","controversial"]:
            raise InvalidSortingType

        if "subreddit" in args:
            print (
                "search for {search}search in\n" \
                "subreddit: {subreddit}\nsort: {sort}\n" \
                "time: {time}\nlimit: {limit}\n".format(
                    search=args["search"],
                    limit=args["limit"],
                    sort=args["sort"],
                    subreddit=args["subreddit"],
                    time=args["time"]
                ).upper()
            )            
            return redditSearcher(
                reddit.subreddit(args["subreddit"]).search(
                    args["search"],
                    limit=args["limit"],
                    sort=args["sort"],
                    time_filter=args["time"]
                )
            )

        elif "multireddit" in args:
            raise NoPrawSupport
        
        elif "user" in args:
            raise NoPrawSupport

        elif "saved" in args:
            raise NoRedditSupoort
    
    if args["sort"] == "relevance":
        raise InvalidSortingType

    if "saved" in args:
        print(
            "saved posts\nuser:{username}\nlimit={limit}\n".format(
                username=config['reddit_username'],
                limit=args["limit"]
            ).upper()
        )
        return redditSearcher(reddit.user.me().saved(limit=args["limit"]))

    if "subreddit" in args:

        if args["subreddit"] == "frontpage":

            print (
                "subreddit: {subreddit}\nsort: {sort}\n" \
                "time: {time}\nlimit: {limit}\n".format(
                    limit=args["limit"],
                    sort=args["sort"],
                    subreddit=args["subreddit"],
                    time=args["time"]
                ).upper()
            )
            return redditSearcher(
                getattr(reddit.front,args["sort"]) (**keyword_params)
            )

        else:  
            print (
                "subreddit: {subreddit}\nsort: {sort}\n" \
                "time: {time}\nlimit: {limit}\n".format(
                    limit=args["limit"],
                    sort=args["sort"],
                    subreddit=args["subreddit"],
                    time=args["time"]
                ).upper()
            )
            return redditSearcher(
                getattr(
                    reddit.subreddit(args["subreddit"]),args["sort"]
                ) (**keyword_params)
            )

    elif "multireddit" in args:
        print (
            "multireddit: {user}, {subreddit}\nsort: {sort}\n" \
            "time: {time}\nlimit: {limit}\n".format(
                user=args["user"],
                limit=args["limit"],
                sort=args["sort"],
                subreddit=args["subreddit"],
                time=args["time"]
            ).upper()
        )
        try:
            return redditSearcher(
                getattr(
                    reddit.multireddit(
                        args["user"], args["multireddit"]
                    ),args["sort"]
                ) (**keyword_params)
            )
        except NotFound:
            raise MultiredditNotFound

    elif "submitted" in args:
        print (
            "submitted posts of {user}\nsort: {sort}\n" \
            "time: {time}\nlimit: {limit}\n".format(
                limit=args["limit"],
                sort=args["sort"],
                user=args["user"],
                time=args["time"]
            ).upper()
        )
        return redditSearcher(
            getattr(
                reddit.redditor(args["user"]).submissions,args["sort"]
            ) (**keyword_params)
        )

    elif "post" in args:
        print("post: {post}\n".format(post=args["post"]).upper())
        return redditSearcher(
            reddit.submission(url=args["post"]),SINGLE_POST=True
        )

def redditSearcher(posts,SINGLE_POST=False):
    """Check posts and decide if it can be downloaded.
    If so, create a dictionary with post details and append them to a list.
    Write all of posts to file. Return the list
    """

    subList = []
    global subCount
    subCount = 0
    global orderCount
    orderCount = 0
    global gfycatCount
    gfycatCount = 0
    global imgurCount
    imgurCount = 0
    global directCount
    directCount = 0

    postsFile = createLogFile("POSTS")

    if SINGLE_POST:
        submission = posts
        subCount += 1 
        try:
            details = {'postId':submission.id,
                       'postTitle':submission.title,
                       'postSubmitter':str(submission.author),
                       'postType':None,
                       'postURL':submission.url,
                       'postSubreddit':submission.subreddit.display_name}
        except AttributeError:
            pass

        postsFile.add({subCount:[details]})
        details = checkIfMatching(submission)

        if details is not None:
            if not details["postType"] == "self":
                orderCount += 1
                printSubmission(submission,subCount,orderCount)
                subList.append(details)
            else:
                postsFile.add({subCount:[details]})

    else:
        for submission in posts:
            subCount += 1

            try:
                details = {'postId':submission.id,
                           'postTitle':submission.title,
                           'postSubmitter':str(submission.author),
                           'postType':None,
                           'postURL':submission.url,
                           'postSubreddit':submission.subreddit.display_name}
            except AttributeError:
                continue

            postsFile.add({subCount:[details]})
            details = checkIfMatching(submission)

            if details is not None:
                if not details["postType"] == "self":
                    orderCount += 1
                    printSubmission(submission,subCount,orderCount)
                    subList.append(details)
                else:
                    postsFile.add({subCount:[details]})

    if not len(subList) == 0:    
        print(
            "\nTotal of {} submissions found!\n"\
            "{} GFYCATs, {} IMGURs and {} DIRECTs\n"
            .format(len(subList),gfycatCount,imgurCount,directCount)
        )
        return subList
    else:
        raise NoMatchingSubmissionFound

def checkIfMatching(submission):
    global gfycatCount
    global imgurCount
    global directCount

    try:
        details = {'postId':submission.id,
                   'postTitle':submission.title,
                   'postSubmitter':str(submission.author),
                   'postType':None,
                   'postURL':submission.url,
                   'postSubreddit':submission.subreddit.display_name}
    except AttributeError:
        return None

    if ('gfycat' in submission.domain) or \
        ('imgur' in submission.domain):

        if 'gfycat' in submission.domain:
            details['postType'] = 'gfycat'
            gfycatCount += 1
            return details

        elif 'imgur' in submission.domain:
            details['postType'] = 'imgur'
            
            imgurCount += 1
            return details

    elif isDirectLink(submission.url) is True:
        details['postType'] = 'direct'
        directCount += 1
        return details

    elif submission.is_self:
        details['postType'] = 'self'
        return details

def printSubmission(SUB,validNumber,totalNumber):
    """Print post's link, title and media link to screen"""

    print(validNumber,end=") ")
    print(totalNumber,end=" ")
    print(
        "https://www.reddit.com/"
        +"r/"
        +SUB.subreddit.display_name
        +"/comments/"
        +SUB.id
    )
    print(" "*(len(str(validNumber))
          +(len(str(totalNumber)))+3),end="")

    try:
        print(SUB.title)
    except:
        SUB.title = "unnamed"
        print("SUBMISSION NAME COULD NOT BE READ")
        pass

    print(" "*(len(str(validNumber))+(len(str(totalNumber)))+3),end="")
    print(SUB.url,end="\n\n")

def isDirectLink(URL):
    """Check if link is a direct image link.
    If so, return True,
    if not, return False
    """

    imageTypes = ['.jpg','.png','.mp4','.webm','.gif']
    if URL[-1] == "/":
        URL = URL[:-1]

    if "i.reddituploads.com" in URL:
        return True

    for extension in imageTypes:
        if extension in URL:
            return True
    else:
        return False
