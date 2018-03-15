from .AnkiConnectorUtils import AnkiConnectorUtils
from ..ankiClasses import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from .. import config


class AnkiConnector:

    def __init__(
            self,
            url=config.defaultAnkiConnectAddress,
            defaultDeck=config.defaultDeck):
        self.url = url  # TODO remove
        self.defaultDeck = defaultDeck
        self.currentDecks = []
        self.connector = AnkiConnectorUtils(self.url)

    def uploadNewDeck(self, deck: AnkiDeck):

        if self.connector.testConnection() != True:
            print(
                "Failed to connect to Anki Connect. Ensure Anki is open and AnkiConnect is installed")
            return False

        self._checkForDefaultDeck()
        self._buildNewDecksAsRequired(deck.getDeckNames())
        # Build new questions
        notes = self._buildNotes(deck.getQuestions())

        # TODO Get all question from that deck and use this to verify questions need to be uploaded
        # self._removeAlreadyExistingQuestions()

        # Insert new question through the api
        self.connector.uploadNotes(notes)

    def _buildNewDecksAsRequired(self, deckNames: [str]):
        # Check decks exist for notes
        newDeckPaths = []
        for i in deckNames:
            fullDeckPath = self._getFullDeckPath(i)
            if fullDeckPath not in self.currentDecks and fullDeckPath not in newDeckPaths:
                newDeckPaths.append(fullDeckPath)

        # Create decks
        for deck in newDeckPaths:
            self.connector.createDeck(deck)

    def _getFullDeckPath(self, deckName: str):
        return self.defaultDeck + "::" + deckName

    def _checkForDefaultDeck(self):
        self.currentDecks = self.connector.getDeckNames()
        if self.defaultDeck not in self.currentDecks:
            self.connector.createDeck(self.defaultDeck)

    def _buildNotes(self, ankiQuestions: [AnkiQuestion]):

        notes = []
        for i in ankiQuestions:
            notes.append(self._buildNote(i))

        finalNotes = {}
        finalNotes["notes"] = notes
        return finalNotes

    def _buildNote(self, ankiQuestion: AnkiQuestion):

        # All decks stored under default deck
        if ankiQuestion.deckName == "" or ankiQuestion.deckName is None:
            # TODO log note was built on default deck
            deckName = self.defaultDeck
        else:
            deckName = self._getFullDeckPath(ankiQuestion.deckName)

        # Convert
        note = {"deckName": deckName, "modelName": "Basic"}
        note["tags"] = ankiQuestion.tags

        # Generate fields
        fields = {}
        fields["Front"] = ankiQuestion.question
        fields["Back"] = self._createAnswerString(ankiQuestion.answers)

        note["fields"] = fields
        return note

    def _createAnswerString(self, answers: [str], bulletPoints: bool=True):
        result = ""
        if not bulletPoints:
            for i in answers:
                result += i + "<br>"  # HTML link break
        else:
            # Can only can create single level of indentation. Align
            # bulletpoints.
            result += "<ul style='list-style-position: inside;'>"
            for i in answers:
                result += "<li>" + i + "</li>"
            result += "</ul>"
        return result


if __name__ == "__main__":

    b = AnkiConnector()

    # TestQuestion
    # q = AnkiQuestion("Test question", "Basic")
    # q.addAnswer("First answer edited")
    # q.addAnswer("Second answer")
    # a = AnkiQuestion("second test question", "Basic")
    # a.addAnswer("First answer")
    # a.addAnswer("Second answer")
    # b.uploadNewQuestions([q])#, a])
