import argparse
import os
from pathlib import Path
from time import localtime, strftime

import praw

from src.tools import GLOBAL, createLogFile, jsonFile, printToFile

print = printToFile

def beginPraw(config,user_agent = "newApp"):
    return praw.Reddit(client_id = config['reddit_client_id'], \
                       client_secret = config['reddit_client_secret'], \
                       password = config['reddit_password'], \
                       user_agent = user_agent, \
                       username = config['reddit_username'])

def getPosts():
    config = GLOBAL.config
    args = GLOBAL.arguments
    
    if GLOBAL.arguments.limit is None:
        PSUDO_LIMIT = "UNLIMITED"
    else:
        PSUDO_LIMIT = GLOBAL.arguments.limit

    print("\nSEARCHING STARTED\n")
    if args.time is None:
        args.time = "all"

    if args.sort == "top" or args.sort == "controversial":
        keyword_params = {
            "time_filter":args.time,
            "limit":args.limit
        }

    else:
         keyword_params = {
             "limit":args.limit
         }

    global HEADER

    if args.saved is True:
        HEADER = (
            "SAVED POSTS OF {username}\n"
            .format(username=config['reddit_username'])
        )
        print(HEADER)
        return redditSearcher(beginPraw(config)
                              .user.me().saved(limit=args.limit))

    elif args.subreddit.lower() == "me":
        HEADER = ("FIRST {limit} {sort} POSTS FROM FRONTPAGE, {time}\n"
                    .format(limit=PSUDO_LIMIT,
                            sort=args.sort.upper(),
                            subreddit=args.subreddit.upper(),
                            time=args.time.upper()))
        print(HEADER)
        return redditSearcher(getattr(beginPraw(config)
                                        .front,args.sort) (**keyword_params))

    else:  
        HEADER = ("FIRST {limit} {sort} POSTS OF R/{subreddit}, {time}\n"
                .format(limit=PSUDO_LIMIT,
                        sort=args.sort.upper(),
                        subreddit=args.subreddit.upper(),
                        time=args.time.upper()))
        print(HEADER)
        return redditSearcher(getattr(beginPraw(config)
                                    .subreddit(args.subreddit),
                                    args.sort) (**keyword_params))

    if args.search is not None:
        if args.subreddit.lower() == "me":
            HEADER = ("SEARCHING FOR {query} IN FIRST {limit} {sort} POSTS FROM FRONTPAGE," \
                    " {time}\n".format(query=args.search.upper(),
                                                    limit=PSUDO_LIMIT,
                                                    sort=args.sort.upper(),
                                                    subreddit=args.subreddit.upper(),
                                                    time=args.time.upper()))
            print(HEADER)
            return redditSearcher(getattr(beginPraw(config).front,
                                          search)(args.search,
                                                  limit=args.limit,
                                                  sort=args.sort,
                                                  time_filter=args.time))
        else:
            HEADER = ("SEARCHING FOR {query} IN FIRST {limit} {sort} POSTS OF R/" \
                  "{subreddit}, {time}\n".format(query=args.search.upper(),
                                                 limit=PSUDO_LIMIT,
                                                 sort=args.sort.upper(),
                                                 subreddit=args.subreddit.upper(),
                                                 time=args.time.upper()))
            print(HEADER)
            return redditSearcher(beginPraw(config).subreddit(args.subreddit)
                                                   .search(args.search,
                                                           limit=args.limit,
                                                           sort=args.sort,
                                                           time_filter=args.time))

def redditSearcher(posts):
    subList = []
    subCount = 0
    orderCount = 0
    gfycatCount = 0
    imgurCount = 0
    directCount = 0
    found = False

    postsFile = createLogFile("POSTS")
    postsFile.add({"HEADER":HEADER})

    for submission in posts:
        subCount += 1
        found = False

        try:
            details = {'postId':submission.id,
                       'postTitle':submission.title,
                       'postSubmitter':str(submission.author),
                       'postType':None,
                       'postURL':submission.url,
                       'postSubreddit':submission.subreddit.display_name}
        except AttributeError:
            continue

        if ('gfycat' in submission.domain) or \
           ('imgur' in submission.domain):
            found = True
            if 'gfycat' in submission.domain:
                details['postType'] = 'gfycat'
                gfycatCount += 1
            elif 'imgur' in submission.domain:
                details['postType'] = 'imgur'
                imgurCount += 1
            orderCount += 1
            printSubmission(submission,subCount,orderCount)

        elif isDirectLink(submission.url) is True:
            found = True
            orderCount += 1
            directCount += 1
            details['postType'] = 'direct'
            printSubmission(submission,subCount,orderCount)

        if found:
            subList.append(details)

        postsFile.add({subCount:[details]})
        
    print(
        "\nTotal of {} submissions found!\n{} GFYCATs, {} IMGURs and {} DIRECTs\n"
        .format(len(subList),gfycatCount,imgurCount,directCount)
    )
    return subList

def createPostsFile():
    logFilename = 'POSTS_'+strftime("%d-%m-%Y_%H-%M-%S", localtime())+'.json'
    if not os.path.exists(Path('logs')):
        os.makedirs(Path('logs'))
    return jsonFile(Path('logs') / Path(logFilename))

def printSubmission(SUB,validNumber,totalNumber):
    print(validNumber,end=") ")
    print(totalNumber,end=" ")
    print("https://www.reddit.com/"+"r/"+SUB.subreddit.display_name+"/comments/"+SUB.id)
    print(" "*(len(str(validNumber))+(len(str(totalNumber)))+3),end="")

    try:
        print(SUB.title)
    except:
        SUB.title = "unnamed"
        print("SUBMISSION NAME COULD NOT BE READ")
        pass

    print(" "*(len(str(validNumber))+(len(str(totalNumber)))+3),end="")
    print(SUB.url,end="\n\n")

def isDirectLink(URL):
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
