#!/usr/bin/env python

"""
This program downloads imgur, gfycat and direct image and video links of 
saved posts from a reddit account. It is written in Python 3.
"""

import argparse
import ctypes
import os
import sys
import time
from pathlib import Path

from src.downloader import Direct, Gfycat, Imgur
from src.searcher import getPosts
from src.tools import (GLOBAL, createLogFile, jsonFile, nameCorrector,
                       printToFile)
from src.errors import (FileAlreadyExistsError, NotADownloadableLinkError,
                        AlbumNotDownloadedCompletely)

__author__ = "Ali Parlakci"
__license__ = "GPL"
__maintainer__ = "Ali Parlakci"
__email__ = "parlakciali@gmail.com"

def debug(*post):
    GLOBAL.config = getConfig('config.json')
    GLOBAL.directory = Path(".\\debug\\")
    downloader([*post])
    quit()

def getConfig(configFileName):
    """Read credentials from config.json file"""

    keys = ['reddit_username',
            'reddit_password',
            'reddit_client_id',
            'reddit_client_secret',
            'imgur_client_id',
            'imgur_client_secret']

    if os.path.exists(configFileName):
        FILE = jsonFile(configFileName)
        content = FILE.read()
        for key in keys:
            try:
                if content[key] == "":
                    raise KeyError
            except KeyError:
                print(key,": ")
                FILE.add({key:input()})
        return jsonFile(configFileName).read()

    else:
        FILE = jsonFile(configFileName)
        configDictionary = {}
        for key in keys:
            configDictionary[key] = input(key + ": ")
        FILE.add(configDictionary)
        return FILE.read()

def parseArguments():
    """Initialize argparse and add arguments"""

    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description="This program downloads " \
                                                 "media from reddit " \
                                                 "posts")
    parser.add_argument("directory",
                        help="Specifies the directory where posts will be " \
                        "downloaded to",
                        metavar="DIRECTORY")

    parser.add_argument("--saved",
                        action="store_true",
                        help="Triggers saved mode")

    parser.add_argument("--log",
                        help="Triggers log read mode and takes a log file",
                        type=argparse.FileType('r'),
                        metavar="LOG FILE")

    parser.add_argument("--subreddit",
                        required="--sort" in sys.argv or \
                                 "--limit" in sys.argv or \
                                 "--search" in sys.argv,
                        nargs="+",
                        help="Triggers subreddit mode and takes subreddit's" \
                             " name without r/. use \"me\" for frontpage",
                        metavar="SUBREDDIT",
                        type=str)
    
    parser.add_argument("--search",
                        help="Searches for given query in given subreddits",
                        type=str)

    parser.add_argument("--sort",
                        help="Either hot, top, new, controversial or rising." \
                             " default: hot",
                        choices=["hot","top","new","controversial","rising"],
                        metavar="SORT TYPE",
                        default="hot",
                        type=str)

    parser.add_argument("--limit",
                        help="default: unlimited",
                        metavar="Limit",
                        default=None,
                        type=int)

    parser.add_argument("--time",
                        help="Either hour, day, week, month, year or all." \
                             " default: all",
                        choices=["all","hour","day","week","month","year"],
                        metavar="TIME_LIMIT",
                        default="all",
                        type=str)
    
    parser.add_argument("--NoDownload",
                        help="Just gets the posts and store them in a file" \
                             " for downloading later",
                        action="store_true",
                        default=False)

    return parser.parse_args()

def checkConflicts():
    """Check if command-line arguments are given correcly,
    if not, raise errors
    """

    if GLOBAL.arguments.saved is False and \
       GLOBAL.arguments.subreddit is None and \
       GLOBAL.arguments.log is None:
        print("NO PROGRAM MODE IS GIVEN\nWhat were you expecting, anyways?")
        quit()

    if GLOBAL.arguments.search is not None and \
       (GLOBAL.arguments.saved is True or \
        GLOBAL.arguments.log is not None):
        print("I cannot search in {}, currently.\nSorry :(".format(mode))
        quit()

def postFromLog(fileName):
    """Analyze a log file and return a list of dictionaries containing
    submissions
    """

    content = jsonFile(fileName).read()

    try:
        del content["HEADER"]
    except KeyError:
        pass

    posts = []

    for post in content:
        if not content[post][-1]['postType'] == None:
            posts.append(content[post][-1])

    return posts

def postExists(POST):
    """Figure out a file's name and checks if the file already exists"""

    title = nameCorrector(POST['postTitle'])
    FILENAME = title + "_" + POST['postId']
    PATH = GLOBAL.directory / POST["postSubreddit"]
    possibleExtensions = [".jpg",".png",".mp4",".gif",".webm"]

    for i in range(2):
        for extension in possibleExtensions:
            FILE_PATH = PATH / (FILENAME+extension)
            if FILE_PATH.exists():
                return True
        else:
            FILENAME = POST['postId']
    else:
        return False

def downloader(submissions):
    """Analyze list of submissions and call the right function
    to download each one, catch errors, update the log files
    """

    directory = GLOBAL.directory
    subsLenght = len(submissions)
    lastRequestTime = 0
    downloadedCount = subsLenght
    duplicates = 0
    BACKUP = {}

    FAILED_FILE = createLogFile("FAILED")

    for i in range(subsLenght):
        print("\n({}/{})".format(i+1,subsLenght))
        print(
            "https://reddit.com/r/{subreddit}/comments/{id}".format(
                subreddit=submissions[i]['postSubreddit'],
                id=submissions[i]['postId']
            )
        )

        if postExists(submissions[i]):
            result = False
            print("It already exists")
            duplicates += 1
            downloadedCount -= 1
            continue

        if submissions[i]['postType'] == 'imgur':
            credit = Imgur.get_credits()
            IMGUR_RESET_TIME = credit['UserReset']-time.time()
            USER_RESET = ("after " \
                          + str(int(IMGUR_RESET_TIME/60)) \
                          + " Minutes " \
                          + str(int(IMGUR_RESET_TIME%60)) \
                          + " Seconds") 
            print(
                "IMGUR => Client: {} - User: {} - Reset {}".format(
                    credit['ClientRemaining'],
                    credit['UserRemaining'],
                    USER_RESET
                )
            )

            if not (credit['UserRemaining'] == 0 or \
                    credit['ClientRemaining'] == 0):
                while int(time.time() - lastRequestTime) <= 2:
                    pass

                lastRequestTime = time.time()

                try:
                    Imgur(GLOBAL.directory / submissions[i]['postSubreddit'],
                          submissions[i])

                except FileAlreadyExistsError:
                    print("It already exists")
                    duplicates += 1
                    downloadedCount -= 1

                except Exception as exception:
                    print(exception)
                    FAILED_FILE.add({int(i+1):[str(exception),submissions[i]]})
                    downloadedCount -= 1

            else:
                if credit['UserRemaining'] == 0:
                    KEYWORD = "user"
                elif credit['ClientRemaining'] == 0:
                    KEYWORD = "client"

                print('{} LIMIT EXCEEDED\n'.format(KEYWORD.upper()))
                FAILED_FILE.add(
                    {int(i+1):['{} LIMIT EXCEEDED\n'.format(KEYWORD.upper()),
                               submissions[i]]}
                )
                downloadedCount -= 1

        elif submissions[i]['postType'] == 'gfycat':
            print("GFYCAT")
            try:
                Gfycat(GLOBAL.directory / submissions[i]['postSubreddit'],
                          submissions[i])

            except FileAlreadyExistsError:
                print("It already exists")
                duplicates += 1
                downloadedCount -= 1
                
            except NotADownloadableLinkError as exception:
                print("Could not read the page source")
                FAILED_FILE.add({int(i+1):[str(exception),submissions[i]]})
                downloadedCount -= 1

            except Exception as exception:
                print(exception)
                FAILED_FILE.add({int(i+1):[str(exception),submissions[i]]})
                downloadedCount -= 1

        elif submissions[i]['postType'] == 'direct':
            print("DIRECT")
            try:
                Direct(GLOBAL.directory / submissions[i]['postSubreddit'],
                          submissions[i])

            except FileAlreadyExistsError:
                print("It already exists")
                downloadedCount -= 1
                duplicates += 1

            except Exception as exception:
                print(exception)
                FAILED_FILE.add({int(i+1):[str(exception),submissions[i]]})
                downloadedCount -= 1
                
        else:
            print("No match found, skipping...")
            downloadedCount -= 1

    if duplicates:
        print("\n There was {} duplicates".format(duplicates))

    if downloadedCount == 0:
        print(" Nothing downloaded :(")

    else:
        print(" Total of {} links downloaded!".format(downloadedCount))

def main():
    GLOBAL.config = getConfig('config.json')

    ####### UNCOMMENT TO DEBUG #######
    # debug({})
    ##################################

    GLOBAL.arguments = parseArguments()

    if GLOBAL.arguments.log is not None:
        GLOBAL.arguments.log = GLOBAL.arguments.log.name

    if GLOBAL.arguments.subreddit is not None:
        GLOBAL.arguments.subreddit = "+".join(GLOBAL.arguments.subreddit)

    GLOBAL.directory = Path(GLOBAL.arguments.directory)

    checkConflicts()

    print(sys.argv)


    if GLOBAL.arguments.NoDownload:
        getPosts()
        quit()

    if GLOBAL.arguments.log is not None:
        logDir = Path(GLOBAL.arguments.log)
        downloader(postFromLog(logDir))

    else:
        downloader(getPosts())
    
if __name__ == "__main__":
    try:
        print = printToFile
        GLOBAL.RUN_TIME = time.time()
        main()
    except KeyboardInterrupt:
        print("\nQUITTING...")
        quit()