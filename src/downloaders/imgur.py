import os
import sys
import time
import urllib.request
from pathlib import Path

from imgurpython import *

from src.tools import GLOBAL, nameCorrector, printToFile

print = printToFile

class Imgur:
    def __init__(self):
        config = GLOBAL.config
        self.imgurClient = ImgurClient(config['imgur_client_id'],
                                       config['imgur_client_secret'])

    def download(self,directory,post):
        self.directory = directory
        content = self.getLink(self.getId(post['postURL']))
        lastRequestTime = time.time()
        if type(content) == dict:
            result = self.getFile(content,post)
            if not (result is None):
                if result is False:
                    return False
                else:
                    return result
        else:
            return content
        
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
            try:
                return {'object':self.imgurClient.get_image(identity['id']),
                        'type':'image'}
            except Exception as exception:
                print(str(exception)+"\n")
                return exception

        elif identity['type'] == 'album':
            try:
                return {'object':self.imgurClient.get_album(identity['id']),
                        'type':'album'}
            except Exception as exception:
                return exception

    def getFile(self,content,post):
        exceptionType = None
        if not os.path.exists(self.directory): os.makedirs(self.directory)
        if content['type'] == 'image':
            try:
                imageURL = content['object'].mp4
            except:
                imageURL = content['object'].link
            title = nameCorrector(post['postTitle'])
            print(title
                  + "_"
                  + post['postId']
                  + imageURL[-4:])
            fileDir = self.directory / (title
                                        + "_"
                                        + post['postId']
                                        + '.'
                                        + imageURL.split('.')[-1])
            tempDir = self.directory / (title
                                        + "_"
                                        + post['postId']
                                        + '.tmp')
            if not (os.path.isfile(fileDir)):
                try:
                    urllib.request.urlretrieve(imageURL,tempDir,
                                            reporthook=dlProgress)
                    os.rename(tempDir,fileDir)
                    print("Downloaded" + " "*10,end="\n\n")
                except FileNotFoundError:
                    fileDir = self.directory / (post['postId']
                                                + "_"
                                                + content['object'].id
                                                + '.'
                                                + imageURL.split('.')[-1])
                    fileDir = self.directory / (post['postId']
                                                + "_"
                                                + content['object'].id
                                                + '.tmp')
                    urllib.request.urlretrieve(imageURL,tempDir,
                                            reporthook=dlProgress)
                    os.rename(tempDir,fileDir)
                    print("Downloaded" + " "*10,end="\n\n")
                except Exception as exception:
                    print("Could not get the file\n")
                    print(exception)
                    exceptionType = exception
            else:
                print("The file already exists" + " "*10,end="\n\n")
                exceptionType = False
        elif content['type'] == 'album':
            images = content['object'].images
            imagesLenght = len(images)
            howManyDownloaded = imagesLenght
            title = nameCorrector(post['postTitle'])
            print(title
                  + "_"
                  + post['postId'],
                  end="\n\n")
            folderDir = self.directory / (title
                                          + "_"
                                          + post['postId'])
            if not os.path.exists(folderDir):
                os.makedirs(folderDir)
            for i in range(imagesLenght):
                try:
                    imageURL = images[i]['mp4']
                except:
                    imageURL = images[i]['link']
                fileName = (str(i+1)
                            + "_"
                            + nameCorrector(str(images[i]['title']))
                            + "_"
                            + images[i]['id'])
                fileDir = folderDir / (fileName + imageURL[-4:])
                tempDir = folderDir / (fileName + ".tmp")
                print("  ({}/{})".format(i+1,imagesLenght))
                print("  {}".format(fileName+imageURL[-4:]))
                if not (os.path.isfile(fileDir)):
                    try:
                        urllib.request.urlretrieve(imageURL,tempDir,
                                                reporthook=dlProgress)
                        os.rename(tempDir,fileDir)
                        print("  Downloaded" + " "*10,end="\n\n")
                    except FileNotFoundError:
                        fileName = (str(i+1) + images[i]['id'])
                        fileDir = folderDir / (fileName + imageURL[-4:])
                        tempDir = folderDir / (fileName + ".tmp")
                        urllib.request.urlretrieve(imageURL,tempDir,
                                                reporthook=dlProgress)
                        os.rename(tempDir,fileDir)
                        print("  Downloaded" + " "*10,end="\n\n")
                    except Exception as exception:
                        print("\n  Could not get the file")
                        print("  " + str(exception) + "\n")
                        exceptionType = exception
                        howManyDownloaded -= 1
                else:
                    print("  The file already exists" + " "*10,end="\n\n")
                    howManyDownloaded -= 1
            if not (howManyDownloaded == imagesLenght):
                 exceptionType = False
        if not (exceptionType is None): return exceptionType

    def get_credits(self):
        return self.imgurClient.get_credits()

def dlProgress(count, blockSize, totalSize):
    downloadedMbs = int(count*blockSize*(10**(-6)))
    fileSize = int(totalSize*(10**(-6)))
    sys.stdout.write("\r{}Mb/{}Mb".format(downloadedMbs,fileSize))
    sys.stdout.write("\b"*len("\r{}Mb/{}Mb".format(downloadedMbs,fileSize)))
    sys.stdout.flush()
