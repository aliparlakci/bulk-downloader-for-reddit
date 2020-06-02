import urllib
import json
import os

from src.utils import GLOBAL, nameCorrector
from src.downloaders.Direct import Direct
from src.downloaders.downloaderUtils import getFile
from src.errors import FileNotFoundError, FileAlreadyExistsError, AlbumNotDownloadedCompletely, NotADownloadableLinkError

class Imgur:

    IMGUR_IMAGE_DOMAIN = "https://i.imgur.com/"

    def __init__(self,directory, post):

        link = post['CONTENTURL']

        if link.endswith(".gifv"):
            link = link.replace(".gifv",".mp4")
            Direct(directory, {**post, 'CONTENTURL': link})
            return None

        try:
            self.rawData = self.getData(link)
        except:
            raise NotADownloadableLinkError("Could not read the page source")

        self.directory = directory
        self.post = post

        if self.isAlbum:
            self.downloadAlbum(self.rawData["album_images"])
        else:
            self.download()

    def downloadAlbum(self, images):
        folderName = GLOBAL.config['filename'].format(**self.post)
        folderDir = self.directory / folderName

        imagesLenght = images["count"]
        howManyDownloaded = 0
        duplicates = 0

        try:
            if not os.path.exists(folderDir):
                os.makedirs(folderDir)
        except FileNotFoundError:
            folderDir = self.directory / self.post['POSTID']
            os.makedirs(folderDir)

        for i in range(imagesLenght):
            imageURL = self.IMGUR_IMAGE_DOMAIN + images[i]["hash"]
            filename = "_".join([
                str(i+1), nameCorrector(images[i]['title']), images[i]['hash']
            ]) + images[i]["ext"]
            shortFilename = str(i+1) + "_" + images[i]['hash']

            print("\n  ({}/{})".format(i+1,imagesLenght))

            try:
                getFile(filename,shortFilename,folderDir,imageURL,indent=2)
                howManyDownloaded += 1
                print()
            except FileAlreadyExistsError:
                print("  The file already exists" + " "*10,end="\n\n")
                duplicates += 1

            except Exception as exception:
                print("\n  Could not get the file")
                print(
                    "  "
                    + "{class_name}: {info}".format(
                        class_name=exception.__class__.__name__,
                        info=str(exception)
                    )
                    + "\n"
                )

        if duplicates == imagesLenght:
            raise FileAlreadyExistsError
        elif howManyDownloaded + duplicates < imagesLenght:
            raise AlbumNotDownloadedCompletely(
                "Album Not Downloaded Completely"
            )           

    def download(self):        
        imageURL = self.IMGUR_IMAGE_DOMAIN + self.rawData["hash"] + self.rawData["ext"]

        extension = self.rawData["ext"]
        filename = GLOBAL.config['filename'].format(**self.post)+extension
        shortFilename = self.post['POSTID']+extension
        
        getFile(filename,shortFilename,self.directory,imageURL)

    @property
    def isAlbum(self):
        if "album_images" in self.rawData:
            if self.rawData["album_images"]["count"] != 1:
                return True
        return False

    @staticmethod 
    def getData(link):
        pageSource = urllib.request.urlopen(link).read().decode("utf8")

        STARTING_STRING = "image               : "
        ENDING_STRING = "group               :"

        STARTING_STRING_LENGHT = len(STARTING_STRING)

        startIndex = pageSource.find(STARTING_STRING) + STARTING_STRING_LENGHT
        endIndex = pageSource.find(ENDING_STRING)

        data = pageSource[startIndex:endIndex].strip()[:-1]

        return json.loads(data)

