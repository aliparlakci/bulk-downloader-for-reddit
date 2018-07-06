# [Bulk Downloader for Reddit](https://aliparlakci.github.io/bulk-downloader-for-reddit)  
This program downloads imgur, gfycat and direct image and video links of saved posts from a reddit account. It is written in Python 3.
  
**PLEASE** post any issue you had with the script to [Issues](https://github.com/aliparlakci/bulk-downloader-for-reddit/issues) tab. Since I don't have any testers or contributers I need your feedback.

## [`py -3 script.py`](#running-the-script)

---

## Table of Contents

- [Requirements](#requirements)
- [Configuring the APIs](#configuring-the-apis)
  - [Creating a reddit app](#creating-a-reddit-app)
  - [Creating an imgur app](#creating-an-imgur-app)
- [Program Modes](#program-modes)
  - [saved mode](#saved-mode)
  - [submitted mode](#submitted-mode)
  - [subreddit mode](#subreddit-mode)
  - [multireddit mode](#multireddit-mode)
  - [link mode](#link-mode)
  - [log read mode](#log-read-mode)
- [Running the script](#running-the-script)
  - [Starting for the first time](#starting-for-the-first-time)
  - [Using the command line arguments](#using-the-command-line-arguments)
  - [Examples](#examples)
- [Changelog](#changelog)
  - [release-1.1.0-prerelease-1](#release-110-prerelease-1)
  - [release-1.0.0](#release-100)
---

## Requirements
- Python 3.x*

You can install Python 3 here: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  
You have to check "**Add Python 3 to PATH**" option when installing in order it to run correctly.

*\*:Although the latest version of python is suggested, you can use 3.6.5 since it runs perfectly on that version*

---

## Configuring the APIs
Because this is not a commercial app, you need to create yourself a reddit and an imgur developer app in order APIs to work.

### Creating a reddit app
* Go to https://www.reddit.com/prefs/apps/
* Under **developer apps**, click on **create another app**
* Enter a name into the **name** field.
* Select **script**
* In **redirect uri** field, enter your reddit profile URL.
* Click **create app** button  
  
Your **reddit_client_id** is on the right of the app's icon. And your **reddit_client_secret** is under that.

### Creating an imgur app
* Go to https://api.imgur.com/oauth2/addclient
* Enter a name into the **Application Name** field.
* Pick **Anonymous usage without user authorization** as an **Authorization type**
* Enter your email into the Email field.
* Correct CHAPTCHA
* Click **submit** button  
  
It should redirect to a page which shows your **imgur_client_id** and **imgur_client_secret**

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
**IMPORTANT** You *MUST* be in the directory where script.py is located when running. Otherwise the program will not run correctly.  
  
**WARNING** *DO NOT* let more than *1* instance of script run as it interferes with IMGUR Request Rate.  
  
### Starting for the first time
**WARNING** When running the script for the first time, it will prompt you to enter your credentials into the *command line* where they might be stored. In order to prevent such behaviour, create a **config.json** file as shown below and enter your credentials inside **double quotes**:  
```json
{
    "reddit_username": "",
    "reddit_password": "",
    "reddit_client_id": "",
    "reddit_client_secret": "",
    "imgur_client_id": "",
    "imgur_client_secret": ""
}
```

### Using the command line arguments

Open up the [terminal](https://www.reddit.com/r/NSFW411/comments/8vtnl8/meta_i_made_reddit_downloader_that_can_download/e1rnbnl) and navigate to where script.py is. If you are unfamiliar with changing directories in terminal see Change Directories in [this article](https://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything).
  
Run the script.py file from terminal with command-line arguments. Here is the help page:  
  
**ATTENTION** Use `.\` for current directory and `..\` for upper directory when using short directories, otherwise it might act weird.

```console
$ py -3 script.py --help
usage: script.py [-h] [--link link] [--auth auth] [--saved] [--submitted]
                 [--log LOG FILE] [--subreddit SUBREDDIT [SUBREDDIT ...]]
                 [--multireddit MULTIREDDIT] [--user USER] [--search SEARCH]
                 [--sort SORT TYPE] [--limit Limit] [--time TIME_LIMIT]
                 [--NoDownload]
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
                        Triggers multreddit mode and takes multreddit's name
                        without r/. use "me" for frontpage
  --user USER           reddit username if needed
  --search SEARCH       Searches for given query in given subreddits
  --sort SORT TYPE      Either hot, top, new, controversial, risingor
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
py -3 script.py C:\\NEW_FOLDER\\ANOTHER_FOLDER --log UNNAMED_FOLDER\\FAILED.json --NoRateLimit
```

```console
py -3 script.py .\\NEW_FOLDER --subreddit gifs pics funny --sort top --NoDownload
```

---

## Changelog
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
