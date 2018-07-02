import os
import sys
import time
import urllib.request
from pathlib import Path

from src.tools import nameCorrector, printToFile

print = printToFile

class Gfycat:
    def __init__(self):
        pass

    def download(self,directory,POST):
        POST['gifURL'] = self.getLink(POST['postURL'])
        if type(POST['gifURL']) is list:
            print("Could not read the page source\n")
            return POST['gifURL'][0]
        else: 
            result = self.getFile(directory,POST)
            if not (result is None):
                if result is False:
                    return False
                else:
                    return result
      
    def getLink(self,
                url,
                query='<source id="mp4Source" src=',
                lineNumber=105):
        if url[-5:] == '.webm' or url[-4:] == '.mp4' or url[-4:] == '.gif':
            return url
        if url[-1:] == '/':
            url = url[:-1]       
        if 'gifs' in url:
            url = "https://gfycat.com/" + url.split('/')[-1]
        try:
            pageSource = (urllib.request 
                          .urlopen(url)
                          .read()
                          .decode()
                          .split('\n'))
        except Exception as exception:
            return [exception]
        try:
            theLine = pageSource[lineNumber]
        except IndexError:
            return ["NOT_A_DOWNLOADABLE_LINK"]

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
            return ["NOT_A_DOWNLOADABLE_LINK"]
        return "".join(link)
    
    def getFile(self,directory,post):
        exceptionType = None
        if not os.path.exists(directory): os.makedirs(directory)
        title = nameCorrector(post['postTitle'])
        print(title
              + "_"
              + post['postId']
              + "."
              + post['gifURL'].split('.')[-1])
        fileDir = directory / (title
                               + "_"
                               + post['postId']
                               + '.'
                               + post['gifURL'].split('.')[-1])
        tempDir = directory / (title
                               + "_"
                               + post['postId']
                               + ".tmp")
        if not (os.path.isfile(fileDir)):
            try:
                urllib.request.urlretrieve(post['gifURL'],
                                           tempDir,
                                           reporthook=dlProgress)
                os.rename(tempDir,fileDir)
                print("Downloaded" + " "*10,end="\n\n")
            except FileNotFoundError:
                tempDir = directory / (post['postId'] + ".tmp")
                fileDir = directory / (post['postId']
                                       + '.'
                                       + post['gifURL'].split('.')[-1])
                urllib.request.urlretrieve(post['gifURL'],
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
