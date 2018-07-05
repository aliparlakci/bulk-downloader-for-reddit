import io
import json
import time
from os import makedirs, path, remove
from pathlib import Path


class GLOBAL:
    """Declare global variables
    """

    RUN_TIME = 0
    config = None
    arguments = None
    directory = None
    printVanilla = print

class jsonFile:
    """ Write and read JSON files

    Use add(self,toBeAdded) to add to files

    Use delete(self,*deletedKeys) to delete keys
    """
    
    FILEDIR = ""

    def __init__(self,FILEDIR):
        self.FILEDIR = FILEDIR
        if not path.exists(self.FILEDIR):
            self.__writeToFile({},create=True)

    def read(self):
        with open(self.FILEDIR, 'r') as f:
            return json.load(f)

    def add(self,toBeAdded):
        """Takes a dictionary and merges it with json file.
        It uses new key's value if a key already exists.
        Returns the new content as a dictionary.
        """

        data = self.read()
        data = {**data, **toBeAdded}
        self.__writeToFile(data)
        return self.read()

    def delete(self,*deleteKeys):
        """Delete given keys from JSON file.
        Returns the new content as a dictionary.
        """

        data = self.read()
        for deleteKey in deleteKeys:
            if deleteKey in data:
                del data[deleteKey]
        else:
            return False
        self.__writeToFile(data)

    def __writeToFile(self,content,create=False):
        if not create:
            remove(self.FILEDIR)
        with open(self.FILEDIR, 'w') as f:
            json.dump(content, f, indent=4)

def redditLinkParser(link):
    shortLink = False
    postPage = False
    subreddit = {}
    postId = ""
    extractedQueries = {}
    
    splitted = link.split("/")

    if splitted[0] == "https:" or splitted[0] == "http:":
        splitted = splitted[2:]
        
    if "redd.it" in splitted:
        shortLink = True
    
    if not (splitted[0].endswith(".com") or \
            splitted[0].endswith("redd.it")):
        print("Not a reddit link")
        return None

    for index in range(len(splitted)):

        # SKIP THE DOMAIN NAME
        if splitted[index].endswith(".com") or \
            splitted[index].endswith("redd.it"):
            continue

        # FOUND A QUERY
        if "?" in splitted[index]:

            # DETERMINE WHATS HAPPENING BEFORE QUERIES
            QUESTION_MARK_INDEX = splitted[index].index("?")
            HEADER = splitted[index][:QUESTION_MARK_INDEX]
            extractedQueries["HEADER"] = HEADER
            QUERIES = splitted[index][QUESTION_MARK_INDEX+1:]

            parsedQueries = QUERIES.split("&")

            for query in parsedQueries:
                query = query.split("=")
                extractedQueries[query[0]] = query[1]
            
            if extractedQueries["HEADER"] == "search":
                del extractedQueries['HEADER']
                try:
                    # CHECK IF FOUND A SUBREDDIT
                    subreddit["name"]

                    subreddit["search"] = extractedQueries
                except:
                    subreddit["name"] = "frontpage"
                    subreddit["search"] = extractedQueries
            else:
                try:
                    # CHECK IF FOUND A SUBREDDIT
                    subreddit["name"]

                    if extractedQueries["HEADER"] == "":
                        del extractedQueries["HEADER"]
                        subreddit["queries"] = extractedQueries
                    else:
                        subreddit[extractedQueries["HEADER"]] = extractedQueries
                except:
                    subreddit["name"] = "frontpage"

                    if extractedQueries["HEADER"] == "":
                        del extractedQueries["HEADER"]
                        subreddit["queries"] = extractedQueries
                    else:
                        subreddit[extractedQueries["HEADER"]] = extractedQueries

        if splitted[index] == "r":
            subredditIndex = index+1
            if not splitted[index+2] == "comments":
                subreddit["name"] = splitted[subredditIndex]
        
        try:
            if splitted[subredditIndex+1] in [
                "hot","top","new","controversial","rising"
                ]:

                subreddit["sort"] = splitted[subredditIndex+1]
        except IndexError:
            pass

        # CHECK IF FOUND A SUBREDDIT
        except NameError:
            if splitted[index] in [
                "hot","top","new","controversial","rising"
                ]:

                    if splitted[index-1].endswith(".com") or \
                       splitted[index-1].endswith("redd.it"):
                        subreddit["name"] = "frontpage"

        if splitted[index] == "comments":
            postPage = True
            idIndex = index+1
            postId = splitted[idIndex]
    
    if postPage:
        print(postId)
    elif not postPage:
        pprint(subreddit)

def createLogFile(TITLE):
    """Create a log file with given name
    inside a folder time stampt in its name
    """

    folderDirectory = GLOBAL.directory / str(time.strftime("%d-%m-%Y_%H-%M-%S",
                                             time.localtime(GLOBAL.RUN_TIME)))
    logFilename = TITLE.upper()+'.json'

    if not path.exists(folderDirectory):
        makedirs(folderDirectory)

    return jsonFile(folderDirectory / Path(logFilename))

def printToFile(*args, **kwargs):
    """Print to both CONSOLE and 
    CONSOLE LOG file in a folder time stampt in the name
    """
    
    TIME = str(time.strftime("%d-%m-%Y_%H-%M-%S",
                             time.localtime(GLOBAL.RUN_TIME)))
    folderDirectory = GLOBAL.directory / TIME
    print(*args,**kwargs)

    if not path.exists(folderDirectory):
        makedirs(folderDirectory)
        
    with io.open(
        folderDirectory / "CONSOLE_LOG.txt","a",encoding="utf-8"
    ) as FILE:
        print(*args, file=FILE, **kwargs) 

def nameCorrector(string):
    """Swap strange characters from given string 
    with underscore (_) and shorten it.
    Return the string
    """

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
