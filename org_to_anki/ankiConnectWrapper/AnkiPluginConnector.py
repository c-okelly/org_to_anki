
class AnkiPluginConnector:

    # TODO => integrate for anki

    def __init__(self, url):
        self.url = url

    def makeRequest(self, action: str, parmeters: dict={}):

        payload = self._buildPayload(action, parmeters)
        if payload.get("action") != "storeMediaFile":
            print("Parameters sent to Anki", payload, "\n")
        else:
            truncateMediaEncoding = copy.deepcopy(payload)
            truncateMediaEncoding.get("params")["data"] = 'encoding remvoed for print statement'
            print("Parameters sent to Anki", truncateMediaEncoding, "\n")

        payload = json.dumps(payload)
        # TODO log payloads
        try:
            res = requests.post(self.url, payload)
        except Exception as e:
            print("An error has occurred make the request.\n", e)

        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            return res.status_code

    def getDeckNames(self):
        result = self.makeRequest("deckNames")
        return self._getResultOrError(result)

    def createDeck(self, deckName: str):
        result = self.makeRequest("createDeck", {"deck": deckName})
        return self._getResultOrError(result)

    def uploadNotes(self, notes: {}):
        result = self.makeRequest("addNotes", notes)
        return self._getResultOrError(result)

    def uploadMediaCollection(self, mediaItems):
        for i in mediaItems:
            self.uploadMedia(i.get("fileName"), i.get("data"))

    def uploadMedia(self, fileName, base64EncodedMedia):
        result = self.makeRequest("storeMediaFile", {"filename": fileName, "data": base64EncodedMedia})
        return self._getResultOrError(result)

    def testConnection(self):
        try:
            # TODO log status code
            return requests.post(self.url, data={}).status_code == 200
        except requests.exceptions.RequestException:
            # TODO log exception
            return False