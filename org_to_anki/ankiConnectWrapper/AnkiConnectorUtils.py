import requests
import json


class AnkiConnectorUtils:

    def __init__(self, url):
        self.url = url

    def makeRequest(self, action: str, parmeters: dict={}):

        payload = self._buildPayload(action, parmeters)
        print("Parameters sent to Anki", payload, "\n")
        # TODO log payloads
        try:
            res = requests.post(self.url, payload)
        except Exception as e:
            print(e)
            print("An error has occoured make the request.")

        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            error = res.status_code
            return error

    def getDeckNames(self):
        result = self.makeRequest("deckNames")
        return self._getResultOrError(result)

    def createDeck(self, deckName: str):
        result = self.makeRequest("createDeck", {"deck": deckName})
        return self._getResultOrError(result)

    def uploadNotes(self, notes: {}):
        result = self.makeRequest("addNotes", notes)
        return self._getResultOrError(result)

    def testConnection(self):
        try:
            res = requests.post(self.url, data={})
            # TODO log status code
            return res.status_code == 200
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
        return json.dumps(payload)


if __name__ == "__main__":
    a = AnkiConnectorUtils("http://127.0.0.1:8765/")
    param = {
        "note": {
            "deckName": "Default",
            "tags": ["yomichan"],
            "modelName": "Basic",
            "fields": {
                "Front": "front content 40",
                "Back": "back content"}}}
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

    result = a.makeRequest("addNotes", param)
    print("Results \n\n")
    print(result)
