# [Bulk Downloader for Reddit](https://aliparlakci.github.io/bulk-downloader-for-reddit)  
This program downloads imgur, gfycat and direct image and video links of saved posts from a reddit account. It is written in Python 3.
  
**PLEASE** post any issue you had with the script to [Issues](https://github.com/aliparlakci/bulk-downloader-for-reddit/issues) tab. Since I don't have any testers or contributers I need your feedback.

---

## Table of Contents

- [Requirements](#requirements)
- [Configuring the APIs](#configuring-the-apis)
  - [Creating an imgur app](#creating-an-imgur-app)
- [Program Modes](#program-modes)
  - [saved mode](#saved-mode)
  - [submitted mode](#submitted-mode)
  - [subreddit mode](#subreddit-mode)
  - [multireddit mode](#multireddit-mode)
  - [link mode](#link-mode)
  - [log read mode](#log-read-mode)
- [Running the script](#running-the-script)
  - [Using the command line arguments](#using-the-command-line-arguments)
  - [Examples](#examples)
- [FAQ](#faq)
- [Changelog](#changelog)
  - [release-1.1.0-prerelease-3](#release-110-prerelease-3)
  - [release-1.1.0-prerelease-2](#release-110-prerelease-2)
  - [release-1.1.0-prerelease-1](#release-110-prerelease-1)
  - [release-1.0.0](#release-100)
  
---

## Requirements
- Python 3.x*

You can install Python 3 here: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  
You have to check "**Add Python 3 to PATH**" option when installing in order it to run correctly.

*\*Although the latest version of python is suggested, you can use 3.6.5 since it runs perfectly on that version*

---

## Configuring the APIs
Because this is not a commercial app, you need to create yourself a reddit and an imgur developer app in order APIs to work.

### Creating an imgur app
* Go to https://api.imgur.com/oauth2/addclient
* Enter a name into the **Application Name** field.
* Pick **Anonymous usage without user authorization** as an **Authorization type**\*
* Enter your email into the Email field.
* Correct CHAPTCHA
* Click **submit** button  
  
It should redirect to a page which shows your **imgur_client_id** and **imgur_client_secret**

  
\*Select **OAuth 2 authorization without a callback URL** first then select **Anonymous usage without user authorization** if it says *Authorization callback URL: required*

---

## Program Modes
All the program modes are activated with command-line arguments as shown [here](#using-the-command-line-arguments)  
### saved mode
In saved mode, the program gets posts from given user's saved posts.
### submitted mode
In submitted mode, the program gets posts from given user's submitted posts.
### subreddit mode
In subreddit mode, the program gets posts from given subreddits* that is sorted by given type and limited by given number.  
  
Multiple subreddits can be given
  
*You may also use search in this mode. See [`py -3 script.py --help`](#using-the-command-line-arguments).*
### multireddit mode
In multireddit mode, the program gets posts from given user's given multireddit that is sorted by given type and limited by given number.  
### link mode
In link mode, the program gets posts from given reddit link.  
  
You may customize the behaviour with `--sort`, `--time`, `--limit`.
  
*You may also use search in this mode. See [`py -3 script.py --help`](#using-the-command-line-arguments).*
  
### log read mode
Two log files are created each time *script.py* runs.
- **POSTS** Saves all the posts without filtering.
- **FAILED** Keeps track of posts that are tried to be downloaded but failed.
  
In log mode, the program takes a log file which created by itself, reads posts and tries downloading them again.

Running log read mode for FAILED.json file once after the download is complete is **HIGHLY** recommended as unexpected problems may occur.

---

## Running the script
**WARNING** *DO NOT* let more than *1* instance of script run as it interferes with IMGUR Request Rate.  
  
### Using the command line arguments
If no arguments are passed program will prompt you for arguments below which means you may start up the script with double-clicking on it (at least on Windows for sure).
  
Open up the [terminal](https://www.reddit.com/r/NSFW411/comments/8vtnl8/meta_i_made_reddit_downloader_that_can_download/e1rnbnl) and navigate to where script.py is. If you are unfamiliar with changing directories in terminal see Change Directories in [this article](https://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything).
  
Run the script.py file from terminal with command-line arguments. Here is the help page:  
  
**ATTENTION** Use `.\` for current directory and `..\` for upper directory when using short directories, otherwise it might act weird.

```console
$ py -3 script.py --help
usage: script.py [-h] [--link link] [--saved] [--submitted] [--log LOG FILE]
                 [--subreddit SUBREDDIT [SUBREDDIT ...]]
                 [--multireddit MULTIREDDIT] [--user redditor]
                 [--search query] [--sort SORT TYPE] [--limit Limit]
                 [--time TIME_LIMIT] [--NoDownload]
                 DIRECTORY

This program downloads media from reddit posts

positional arguments:
  DIRECTORY             Specifies the directory where posts will be downloaded
                        to

optional arguments:
  -h, --help            show this help message and exit
  --link link, -l link  Get posts from link
  --auth.               2FA key
  --saved               Triggers saved mode
  --submitted           Gets posts of --user
  --log LOG FILE        Triggers log read mode and takes a log file
  --subreddit SUBREDDIT [SUBREDDIT ...]
                        Triggers subreddit mode and takes subreddit's name
                        without r/. use "frontpage" for frontpage
  --multireddit MULTIREDDIT
                        Triggers multireddit mode and takes multireddit's name
                        without m/
  --user redditor       reddit username if needed. use "me" for current user
  --search query        Searches for given query in given subreddits
  --sort SORT TYPE      Either hot, top, new, controversial, rising or
                        relevance default: hot
  --limit Limit         default: unlimited
  --time TIME_LIMIT     Either hour, day, week, month, year or all. default:
                        all
  --NoDownload          Just gets the posts and store them in a file for
                        downloading later
```  
  
---


## Examples

```console
py -3 script.py .\\NEW_FOLDER --sort all --limit 10 --link "https://www.reddit.com/r/gifs/search?q=dogs&restrict_sr=on&type=link&sort=new&t=month"
```

```console
py -3 script.py .\\NEW_FOLDER --sort all --limit 10 --link "https://www.reddit.com/r/learnprogramming/comments/8wzc7y/"
```

```console
py -3 script.py .\\NEW_FOLDER --sort all --limit 10 --link "www.reddit.com/top/"
```

```console
py -3 script.py .\\NEW_FOLDER --search cats --limit 10 --link "www.reddit.com/hot/"
```
  
```console
py -3 script.py .\\NEW_FOLDER --subreddit gifs --sort hot --search cats
```

```console
py -3 script.py .\\NEW_FOLDER --subreddit frontpage --sort top --search cats
```

```console
py -3 script.py .\\NEW_FOLDER --multireddit good_subs --user [USER_NAME] --sort top --time week --limit 250
```

```console
py -3 script.py .\\NEW_FOLDER\\ANOTHER_FOLDER --saved --limit 1000
```

```console
py -3 script.py C:\\NEW_FOLDER\\ANOTHER_FOLDER --log UNNAMED_FOLDER\\FAILED.json
```

```console
py -3 script.py .\\NEW_FOLDER --subreddit gifs pics funny --sort top --NoDownload
```

---

## FAQ
### I can't startup the script no matter what.
- Try `python3` or `python` or `py -3` as python have real issues about naming their program

---

## Changelog
### [release-1.1.0-prerelease-3](https://github.com/aliparlakci/bulk-downloader-for-reddit/releases/tag/release-1.1.0-prerelease-3)

- Give an error message if no posts found in given URL in link mode
- Print out the Authorization URL for reddit if browser window fails to open
- Bug fixes, especially in search mode

### [release-1.1.0-prerelease-2](https://github.com/aliparlakci/bulk-downloader-for-reddit/releases/tag/release-1.1.0-prerelease-2)

- Now using web app.
- Detecting argument conflicts improved
- "me" can now be used to resemble current user logged in
- If no arguments passed when starting up the program, it prompts for arguments now
- Fixed bug that causes search links not to work
- Fixed log file mode bug
- Bug fixes

### [release-1.1.0-prerelease-1](https://github.com/aliparlakci/bulk-downloader-for-reddit/releases/tag/release-1.1.0-prerelease-1)
  
- Added link mode
  - It can parse reddit links now
- Added multireddit mode
  - It can get posts from multireddits now
- Added submitted mode
  - It can get posts from user's posts now
- Added search options for suitable modes
- Detects argument conflicts more accurately
- Added support for Two Factor Authorization
- Bug fixes

### [release-1.0.0](https://github.com/aliparlakci/bulk-downloader-for-reddit/releases/tag/release-1.0)
- Initial release
