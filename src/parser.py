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
    
    elif ("me" in SplittedLink or \
          "u" in SplittedLink or \
          "user" in SplittedLink or \
          "r" in SplittedLink) and \
          "m" in SplittedLink:

        if not "r" in SplittedLink:

            for index in range(len(SplittedLink)):
                if SplittedLink[index] == "u" or \
                   SplittedLink[index] == "user":
                    RESULT["user"] = SplittedLink[index+1]

                if SplittedLink[index] in ["posts", "saved", "upvoted","m"]:
                    RESULT[SplittedLink[index]] = RESULT["user"]
                    del RESULT["user"]

        elif "m" in SplittedLink:
            RESULT["m"] = SplittedLink.index("m") + 1
            RESULT["user"] = "me"

        else:
            for index in range(len(SplittedLink)):

                if SplittedLink[index] == "r":
                    RESULT["subreddit"] = SplittedLink[index+1]

                if SplittedLink[index] in [
                    "hot","top","new","controversial","rising"
                    ]:

                    RESULT["sort"] = SplittedLink[index]

                    if index - 1 == 0:
                        RESULT["subreddit"] = "frontpage"    

        for index in range(len(SplittedLink)):
            if SplittedLink[index] in [
                    "hot","top","new","controversial","rising"
                    ]:

                    RESULT["sort"] = SplittedLink[index]

                    if index - 1 == 0:
                        RESULT["subreddit"] = "frontpage"

            elif "?" in SplittedLink[index]:
                ParsedQuery = QueryParser(SplittedLink[index],index)
                if ParsedQuery["HEADER"] == "search":
                    del ParsedQuery["HEADER"]
                    RESULT["search"] = ParsedQuery

                else:
                    del ParsedQuery["HEADER"]
                    RESULT["queries"] = ParsedQuery

    return RESULT

if __name__ == "__main__":
    while True:
        pprint(LinkParser(input("> ")))