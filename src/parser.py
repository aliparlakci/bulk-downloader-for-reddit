from pprint import pprint

def QueryParser(PassedQueries,index):
    ExtractedQueries = {}

    QuestionMarkIndex = PassedQueries.index("?")
    Header = PassedQueries[:QuestionMarkIndex]
    ExtractedQueries["HEADER"] = Header
    Queries = PassedQueries[QuestionMarkIndex+1:]

    ParsedQueries = Queries.split("&")

    for Query in ParsedQueries:
        Query = Query.split("=")
        ExtractedQueries[Query[0]] = Query[1]

    if ExtractedQueries["HEADER"] == "search":
        ExtractedQueries["q"] = ExtractedQueries["q"].replace("%20"," ")

    return ExtractedQueries

def LinkParser(LINK):
    RESULT = {}
    ShortLink = False

    SplittedLink = LINK.split("/")

    if SplittedLink[0] == "https:" or SplittedLink[0] == "http:":
        SplittedLink = SplittedLink[2:]

    if "redd.it" in SplittedLink:
        ShortLink = True

    if not SplittedLink[0].endswith("reddit.com"):
        return None
    else:
        SplittedLink = SplittedLink[1:]
    
    if "comments" in SplittedLink:
        idIndex = SplittedLink.index("comments")
        RESULT = {"post":SplittedLink[idIndex+1]}
    
    elif "me" in SplittedLink or \
         "u" in SplittedLink or \
         "user" in SplittedLink or \
         "r" in SplittedLink or \
         "m" in SplittedLink:

        if not "r" in SplittedLink:

            for index in range(len(SplittedLink)):
                if SplittedLink[index] == "u" or \
                   SplittedLink[index] == "user":

                    RESULT["user"] = SplittedLink[index+1]

                elif SplittedLink[index] == "me":
                    RESULT["user"] = "me"

        if "m" in SplittedLink:
            RESULT["multireddit"] = SplittedLink[SplittedLink.index("m") + 1]
            RESULT["user"] = SplittedLink[SplittedLink.index("m") - 1]

    for index in range(len(SplittedLink)):
        if SplittedLink[index] in [
            "hot","top","new","controversial","rising"
            ]:

            RESULT["sort"] = SplittedLink[index]

            if index == 0:
                RESULT["subreddit"] = "frontpage"
        
        elif SplittedLink[index] in ["submitted","saved","posts"]:
            if SplittedLink[index] == "submitted":
                RESULT[SplittedLink[index]] = {}
            
            elif SplittedLink[index] == "posts":
                RESULT["submitted"] = {}

            elif SplittedLink[index] == "saved":
                RESULT["saved"] == True

        elif "?" in SplittedLink[index]:
            ParsedQuery = QueryParser(SplittedLink[index],index)
            if ParsedQuery["HEADER"] == "search":
                del ParsedQuery["HEADER"]
                RESULT["search"] = ParsedQuery

            elif ParsedQuery["HEADER"] == "submitted":
                del ParsedQuery["HEADER"]
                RESULT["submitted"] = ParsedQuery

            else:
                del ParsedQuery["HEADER"]
                RESULT["queries"] = ParsedQuery

    return RESULT

def LinkDesigner(LINK):

    attributes = LinkParser(LINK)
    MODE = {}

    if "search" in attributes:
        MODE["search"] = attributes["search"]["q"]

        if "restrict_sr" in attributes["search"]:
            
            if not (attributes["search"]["restrict_sr"] == 0 or \
                    attributes["search"]["restrict_sr"] == "off"):

                if "subreddit" in attributes:
                    MODE["subreddit"] = attributes["subreddit"]
                elif "multireddit" in attributes:
                    MODE["multreddit"] = attributes["multireddit"]
                    MODE["user"] = attributes["user"]
            else:
                MODE["subreddit"] = "all"
        else:
            MODE["subreddit"] = "all"

        if "t" in attributes["search"]:
            MODE["time"] = attributes["search"]["sort"]
        else:
            MODE["time"] = "all"

        if "sort" in attributes["search"]:
            MODE["sort"] = attributes["search"]["sort"]
        else:
            MODE["sort"] = "relevance"
        
        if "include_over_18" in attributes["search"]:
            if attributes["search"]["include_over_18"] == 1 or \
               attributes["search"]["include_over_18"] == "on":
                MODE["nsfw"] = True
            else:
                MODE["nsfw"] = False

    else:
        if "queries" in attributes:
            if not ("submitted" in attributes or \
                    "posts" in attributes):

                if "t" in attributes["queries"]:
                    MODE["time"] = attributes["queries"]["t"]
                else:
                    MODE["time"] = "day"
            else:
                if "t" in attributes["queries"]:
                    MODE["time"] = attributes["queries"]["t"]
                else:
                    MODE["time"] = "all"

                if "sort" in attributes["queries"]:
                    MODE["sort"] = attributes["queries"]["sort"]
                else:
                    MODE["sort"] = "new"
        else:
            MODE["time"] = "day"
    
    if "sort" in attributes:
        MODE["sort"] = attributes["sort"]
    elif "sort" in MODE:
        pass
    else:
        MODE["sort"] = "hot"
                
    if "subreddit" in attributes and not "search" in attributes:
        MODE["subreddit"] = attributes["subreddit"]

    elif "user" in attributes and not "search" in attributes:
        MODE["user"] = attributes["user"]

        if "submitted" in attributes:
            if "sort" in attributes["submitted"]:
                MODE["sort"] = attributes["submitted"]["sort"]
            elif "sort" in MODE:
                pass
            else:
                MODE["sort"] = "hot"

            if "t" in attributes["submitted"]:
                MODE["time"] = attributes["submitted"]["t"]
            else:
                MODE["time"] = ""
        
        elif "saved" in attributes:
            MODE["saved"] == True
        
        elif "multireddit" in attributes:
            MODE["multireddit"] = attributes["multireddit"]

    return MODE

if __name__ == "__main__":
    while True:
        link = input("> ")
        pprint(LinkDesigner(link))