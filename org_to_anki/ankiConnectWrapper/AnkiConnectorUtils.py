import requests
import json
import copy


class AnkiConnectorUtils:

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
            print("An error has occoured make the request.\n", e)

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
            # TODO log excpetion
            return False

    @staticmethod
    def _getResultOrError(result: {}):
        if result.get("error") is None:
            return result.get("result")
        else:
            return result.get("error")

    @staticmethod
    def _buildPayload(action, params: {}={}, version: int=5):
        payload = {}
        payload["action"] = action
        payload["params"] = params
        payload["version"] = version
        return payload


if __name__ == "__main__":
    a = AnkiConnectorUtils("http://127.0.0.1:8765/")
    param = {"notes": [{"deckName": "Default",
                        "tags": [],
                        "modelName": "Basic",
                        "fields": {"Front": "front content 20s0",
                                   "Back": "back content00100"}},
                       {"deckName": "Default",
                        "tags": ["yomichan"],
                        "modelName": "Basic",
                        "fields": {"Front": "",
                                   "Back": ""}}]}

    print("Results \n", a.makeRequest("addNotes", param))
