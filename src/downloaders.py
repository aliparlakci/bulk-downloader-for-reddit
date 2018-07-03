import os
import sys
import time
import urllib.request
from pathlib import Path

from imgurpython import *

from src.tools import GLOBAL, nameCorrector, printToFile
from src.errors import (FileAlreadyExistsError, NotADownloadableLinkError,
                        AlbumNotDownloadedCompletely)

print = printToFile

def dlProgress(count, blockSize, totalSize):
    downloadedMbs = int(count*blockSize*(10**(-6)))
    fileSize = int(totalSize*(10**(-6)))
    sys.stdout.write("\r{}Mb/{}Mb".format(downloadedMbs,fileSize))
    sys.stdout.write("\b"*len("\r{}Mb/{}Mb".format(downloadedMbs,fileSize)))
    sys.stdout.flush()

def getExtension(link):
    imageTypes = ['jpg','png','mp4','webm','gif']
    parsed = link.split('.')
    if not parsed in imageTypes:
        return '.jpg'
    return "."+parsed[-1]

def getFile(fileDir,tempDir,imageURL,redditID,indent=0):
    if not (os.path.isfile(fileDir)):
        for i in range(3):
            try:
                urllib.request.urlretrieve(imageURL,
                                           tempDir,
                                           reporthook=dlProgress)
                os.rename(tempDir,fileDir)
                print(" "*indent+"Downloaded"+" "*10,end="\n\n")
                break
            except ConnectionResetError as exception:
                print(" "*indent + exception)
                print(" "*indent + "Trying again\n")
            # except FileNotFoundError:
            #    File name is too long, make it short
    else:
        raise FileAlreadyExistsError

class Imgur:
    def __init__(self,directory,post):
        self.imgurClient = self.initImgur()

        imgurID = self.getId(post['postURL'])
        content = self.getLink(imgurID)

        if not os.path.exists(directory): os.makedirs(directory)

        if content['type'] == 'image':

            try:
                post['mediaURL'] = content['object'].mp4
            except AttributeError:
                post['mediaURL'] = content['object'].link

            post['postExt'] = getExtension(post['mediaURL'])

            title = nameCorrector(post['postTitle'])
            print(title+"_" +post['postId']+post['postExt'])

            fileDir = title + "_" + post['postId'] + post['postExt']
            fileDir = directory / fileDir

            tempDir = title + "_" + post['postId'] + '.tmp'
            tempDir = directory / tempDir

            getFile(fileDir,tempDir,post['mediaURL'],post['postId'])

        elif content['type'] == 'album':
            exceptionType = ""
            images = content['object'].images
            imagesLenght = len(images)
            howManyDownloaded = imagesLenght
            duplicates = 0

            title = nameCorrector(post['postTitle'])
            print(title+"_"+post['postId'],end="\n\n")

            folderDir = directory / (title+"_"+post['postId'])

            if not os.path.exists(folderDir):
                os.makedirs(folderDir)

            for i in range(imagesLenght):
                try:
                    imageURL = images[i]['mp4']
                except KeyError:
                    imageURL = images[i]['link']

                images[i]['Ext'] = getExtension(imageURL)

                fileName = (str(i+1)
                            + "_"
                            + nameCorrector(str(images[i]['title']))
                            + "_"
                            + images[i]['id'])

                fileDir = folderDir / (fileName + images[i]['Ext'])
                tempDir = folderDir / (fileName + ".tmp")

                print("  ({}/{})".format(i+1,imagesLenght))
                print("  {}".format(fileName+images[i]['Ext']))

                try:
                    getFile(fileDir,tempDir,imageURL,post['postId'],indent=2)
                except FileAlreadyExistsError:
                    print("  The file already exists" + " "*10,end="\n\n")
                    duplicates += 1
                    howManyDownloaded -= 1
                except Exception as exception:
                    print("\n  Could not get the file")
                    print("  " + str(exception) + "\n")
                    exceptionType = exception
                    howManyDownloaded -= 1

            if duplicates == imagesLenght:
                raise FileAlreadyExistsError
            elif howManyDownloaded < imagesLenght:
                raise AlbumNotDownloadedCompletely
    
    @staticmethod
    def initImgur():
        config = GLOBAL.config
        return ImgurClient(config['imgur_client_id'],
                           config['imgur_client_secret'])

    def getId(self,submissionURL):
        domainLenght = len("imgur.com/")
        if submissionURL[-1] == "/":
            submissionURL = submissionURL[:-1]

        if "a/" in submissionURL or "gallery/" in submissionURL:
            albumId = submissionURL.split("/")[-1]
            return {'id':albumId, 'type':'album'}

        else:
            url = submissionURL.replace('.','/').split('/')
            imageId = url[url.index('com')+1]
            return {'id':imageId, 'type':'image'}

    def getLink(self,identity):
        if identity['type'] == 'image':
            return {'object':self.imgurClient.get_image(identity['id']),
                    'type':'image'}
        elif identity['type'] == 'album':
            return {'object':self.imgurClient.get_album(identity['id']),
                    'type':'album'}

    def get_credits():
        return Imgur.initImgur().get_credits()

class Gfycat:
    def __init__(self,directory,POST):
        try:
            POST['mediaURL'] = self.getLink(POST['postURL'])
        except IndexError:
            raise NotADownloadableLinkError
        except Exception as exception:
            raise NotADownloadableLinkError

        POST['postExt'] = getExtension(POST['mediaURL'])

        try:
            if not os.path.exists(directory): os.makedirs(directory)
            title = nameCorrector(POST['postTitle'])
            print(title+"_"+POST['postId']+POST['postExt'])

            fileDir = title+"_"+POST['postId']+POST['postExt']
            fileDir = directory / fileDir

            tempDir = title+"_"+POST['postId']+".tmp"
            tempDir = directory / tempDir

            getFile(fileDir,tempDir,POST['mediaURL'],POST['postId'])
        except FileAlreadyExistsError:
            raise
      
    def getLink(self, url, query='<source id="mp4Source" src=', lineNumber=105):
        if '.webm' in url or '.mp4' in url or '.gif' in url:
            return url

        if url[-1:] == '/':
            url = url[:-1]

        if 'gifs' in url:
            url = "https://gfycat.com/" + url.split('/')[-1]

        pageSource = (urllib.request.urlopen(url).read().decode().split('\n'))

        theLine = pageSource[lineNumber]
        lenght = len(query)
        link = []

        for i in range(len(theLine)):
            if theLine[i:i+lenght] == query:
                cursor = (i+lenght)+1
                while not theLine[cursor] == '"':
                    link.append(theLine[cursor])
                    cursor += 1
                break

        if "".join(link) == "":
            raise NotADownloadableLinkError

        return "".join(link)

class Direct:
    def __init__(self,directory,POST):
        POST['postExt'] = getExtension(POST['postURL'])
        try:
            if not os.path.exists(directory): os.makedirs(directory)
            title = nameCorrector(POST['postTitle'])
            print(title+"_"+POST['postId']+POST['postExt'])

            fileDir = title+"_"+POST['postId']+POST['postExt']
            fileDir = directory / fileDir

            tempDir = title+"_"+POST['postId']+".tmp"
            tempDir = directory / tempDir

            getFile(fileDir,tempDir,POST['postURL'],POST['postId'])
        except FileAlreadyExistsError:
            raise

