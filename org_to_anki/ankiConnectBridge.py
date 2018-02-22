import requests
import json
from AnkiQuestion import AnkiQuestion

class AnkiConnectBridge:
    def __init__(self, url="http://127.0.0.1:8765/", defaultDeck = "Org Notes"):
        self.url = url
        self.defaultDeck = defaultDeck

    def uploadNewQuestions(self, questions):
        # Check the default deck exists
        decks = self._getDeckNames()
        if tagrgetDeck not in decks:
            self._createDeck(defaultDeck)

        # TODO Get all question from that deck and use this to verify questions need to be uploaded

        # Build new questions
        # Insert new question through the api


    def _makeRequest(self, action, parmeters={}):

        payload = self._buildPayload(action, parmeters)
        res = requests.post(self.url, payload)

        results = None
        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            error = res.status_code
            return error


    def _getDeckNames(self):
        decks = self._makeRequest("deckNames")
        return decks
    
    def _createDeck(self, deckName):
        decks = self._makeRequest("createDeck", {"deck": deckName})
        return decks

    def _buildNote(self, ankiQuestion, deckName=self.defaultDeck):

        if isinstance(ankiQuestion, AnkiQuestion):
            # Convert
            note = {"deckName": deckName, "modelName": "Basic"}
            notes["tags"] = ankiQuestion.tags

            # Generate fields
            fields = {}
            fields["Front"] = ankiQuestion.question
            fields["Back"] = self._createAnswerString(ankiQuestion.answers)

        else:
            # TODO log issue
            raise Exception("Object %s is not an instance of AnkiQuestion and cannot be converted to note" % (ankiQuestion))
    
    def _createAnswerString(self, answers, bulletPoints=False):
        result = ""
        if bulletPoints == False:
            for i in answers:
                result += i + "\n"
        else:
            for i in answers:
                result += "* " + i + "\n"


    # TODO add card
    # TODO add cards

        # payload = {
        #     "action": "notesInfo",
        #     "version": "5",
        #     "params": {
        #         "notes": [1516380924790, 1516381006960]
        #     }
        # }

    def _buildPayload(self, action, params={}, version=5):
        payload = {}
        payload["action"] = action
        payload["params"] = params
        payload["version"] = version
        return json.dumps(payload)

if __name__ == "__main__":

    print("start")
    b = AnkiConnectBridge()
    b._getDeckNames()
    q = AnkiQuestion("Test question")
    q.addAnswer("First answer")
    q.addAnswer("Second answer")
    print(b._buildNote(q))
