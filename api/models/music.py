class Music:
    def __init__(self, dict):
        dict.pop("lyrics", None)
        dict.pop("playlistId", None)
        dict.pop("category", None)
        dict.pop("duration_seconds", None)
        dict.pop("feedbackTokens", None)
        dict.pop("isExplicit", None)
        dict.pop("year", None)
        dict.pop("resultType", None)
        if dict.get("tracks") != None:
            for element in dict["tracks"]:
                if element.get("thumbnails") != None \
                        and element.get("duration") != None:
                    element["thumbnail"] = element["thumbnails"]
                    element["length"] = element["duration"]
                    del element["thumbnails"], element["duration"]
        else:
            if dict.get("thumbnails") != None and dict.get("duration") != None:
                dict["thumbnail"] = dict["thumbnails"]
                dict["length"] = dict["duration"]
                del dict["thumbnails"], dict["duration"]
        self.dict = dict
