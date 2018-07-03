import io
import json
import time
from os import makedirs, path, remove
from pathlib import Path


class GLOBAL:
    RUN_TIME = 0
    config = None
    arguments = None
    directory = None
    printVanilla = print

class jsonFile:
    FILEDIR = ""

    def __init__(self,FILEDIR):
        self.FILEDIR = FILEDIR
        if not path.exists(self.FILEDIR):
            self.__writeToFile({},create=True)

    def read(self):
        with open(self.FILEDIR, 'r') as f:
            return json.load(f)

    def add(self,toBeAdded):
        data = self.read()
        data = {**data, **toBeAdded}
        self.__writeToFile(data)
        return self.read()

    def delete(self,deletedKeys):
        data = self.read()
        if type(deletedKeys) is str:
            if deletedKeys in data:
                del data[deletedKeys]
                self.__writeToFile(data)
            else:
                return False
        elif type(deletedKeys) is list:
            for deletedKey in deletedKeys:
                if deletedKey in data:
                    del data[deletedKey]
            else:
                return False
            self.__writeToFile(data)

    def __writeToFile(self,content,create=False):
        if not create:
            remove(self.FILEDIR)
        with open(self.FILEDIR, 'w') as f:
            json.dump(content, f, indent=4)

def createLogFile(TITLE):
    folderDirectory = GLOBAL.directory / str(time.strftime("%d-%m-%Y_%H-%M-%S",
                                            time.localtime(GLOBAL.RUN_TIME)))
    logFilename = TITLE.upper()+'.json'

    if not path.exists(folderDirectory):
        makedirs(folderDirectory)

    return jsonFile(folderDirectory / Path(logFilename))

def printToFile(TEXT, *args, **kwargs):
    TIME = str(time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime(GLOBAL.RUN_TIME)))
    folderDirectory = GLOBAL.directory / TIME
    print(str(TEXT),*args,**kwargs)

    if not path.exists(folderDirectory):
        makedirs(folderDirectory)
        
    with io.open(folderDirectory / "CONSOLE_LOG.txt","a",encoding="utf-8") as FILE:
        print(str(TEXT),file=FILE, *args, **kwargs) 

def nameCorrector(string):
    stringLenght = len(string)
    if stringLenght > 200:
        string = string[:200]
    stringLenght = len(string)
    spacesRemoved = []

    for b in range(stringLenght):
        if string[b] == " ":
            spacesRemoved.append("_")
        else:
            spacesRemoved.append(string[b])
    
    string = ''.join(spacesRemoved)
    correctedString = []
    
    if len(string.split('\n')) > 1:
        string = "".join(string.split('\n'))

    if '\\' in string or \
    '/' in string or \
    ':' in string or \
    '*' in string or \
    '?' in string or \
    '"' in string or \
    '<' in string or \
    '>' in string or \
    '|' in string or \
    '.' in string:
        for a in range(len(string)):
            if string[a] == '\\' or \
            string[a] == '/' or \
            string[a] == ':' or \
            string[a] == '*' or \
            string[a] == '?' or \
            string[a] == '"' or \
            string[a] == '<' or \
            string[a] == '>' or \
            string[a] == '|' or \
            string[a] == '.':
                correctedString.append("_")
            else:
                correctedString.append(string[a])
        return ''.join(correctedString)    
    else:
        return string
