import os
import sys
import time
import urllib.request
from pathlib import Path

from src.tools import GLOBAL, nameCorrector, printToFile

print = printToFile

class Direct:
    def __init__(self):
        pass
    
    def download(self,directory,post):
        post['postExt'] = self.getExtension(post['postURL'])
        result = self.getFile(directory,post)
        if not (result is None):
            if result is False:
                return False
            else:
                return result
                
    def getExtension(self,link):
        imageTypes = ['jpg','png','mp4','webm','gif']
        parsed = link.split('.')
        if not parsed in imageTypes:
            return 'jpg'
        return parsed[-1]

    def getFile(self,directory,post):
        if not os.path.exists(directory): os.makedirs(directory)
        exceptionType = None
        title = nameCorrector(post['postTitle'])
        print(title
              + "_"
              + post['postId']
              + "."
              + post['postExt'])
        fileDir = directory / (title
                               + "_"
                               + post['postId']
                               + '.'
                               + post['postExt'])
        tempDir = directory / (title
                               + "_"
                               + post['postId']
                               + ".tmp")
        if not (os.path.isfile(fileDir)):
            try:
                urllib.request.urlretrieve(post['postURL'],
                                           tempDir,
                                           reporthook=dlProgress)
                os.rename(tempDir,fileDir)
                print("Downloaded" + " "*10,end="\n\n")
            except FileNotFoundError:
                tempDir = directory / (post['postId'] + ".tmp")
                fileDir = directory / (post['postId'] + '.' + post['postExt'])
                urllib.request.urlretrieve(post['postURL'],
                                           tempDir,
                                           reporthook=dlProgress)
                os.rename(tempDir,fileDir)
                print("Downloaded" + " "*10,end="\n\n")
            except Exception as exception:
                print("Could not get the file")
                print(exception,"\n")
                return exception
        else:
            print("The file already exists" + " "*10,end="\n\n")
            exceptionType = False
        if not (exceptionType is None): return exceptionType

def dlProgress(count, blockSize, totalSize):
    downloadedMbs = int(count*blockSize*(10**(-6)))
    fileSize = int(totalSize*(10**(-6)))
    sys.stdout.write("\r{}Mb/{}Mb".format(downloadedMbs,fileSize))
    sys.stdout.write("\b"*len("\r{}Mb/{}Mb".format(downloadedMbs,fileSize)))
    sys.stdout.flush()
