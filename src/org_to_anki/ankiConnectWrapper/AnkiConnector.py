from .AnkiConnectorUtils import AnkiConnectorUtils
from ..ankiClasses import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from .AnkiNoteBuilder import AnkiNoteBuilder
from .. import config
import base64


class AnkiConnector:

    def __init__(
            self,
            url=config.defaultAnkiConnectAddress,
            defaultDeck=config.defaultDeck):
        self.url = url  # TODO remove
        self.defaultDeck = defaultDeck
        self.oldDefaulDeck = defaultDeck
        self.currentDecks = []
        self.connector = AnkiConnectorUtils(self.url)
        self.AnkiNoteBuilder = AnkiNoteBuilder()

    def uploadNewDeck(self, deck): # (AnkiDeck)

        if self.connector.testConnection() is not True:
            print(
                "Failed to connect to Anki Connect. \
                Ensure Anki is open and AnkiConnect is installed")
            return False

        # Check if should use base deck
        if deck.getParameter("baseDeck", "true").lower() == "false": 
            self.defaultDeck = None
        else:
            self.defaultDeck = self.oldDefaulDeck

        self._checkForDefaultDeck()
        self._buildNewDecksAsRequired(deck.getDeckNames())
        # Build new questions
        notes = self.buildAnkiNotes(deck.getQuestions())
        media = self.prepareMedia(deck.getMedia())

        # TODO Get all question from that deck and
        # use this to verify questions need to be uploaded
        # self._removeAlreadyExistingQuestions()

        # Insert new question through the api
        self.connector.uploadNotes(notes)
        self.connector.uploadMediaCollection(media)

    def prepareMedia(self, ankiMedia): # ([])

        formattedMedia = []
        if len(ankiMedia) == 0:
            return formattedMedia
        else:
            for i in ankiMedia:
                formattedMedia.append({"fileName": i.fileName, "data": base64.b64encode(i.data).decode("utf-8")})
        return formattedMedia

    def _buildNewDecksAsRequired(self, deckNames): # ([str])
        # Check decks exist for notes
        newDeckPaths = []
        for i in deckNames:
            fullDeckPath = self._getFullDeckPath(i)
            if fullDeckPath not in self.currentDecks and fullDeckPath not in newDeckPaths:
                newDeckPaths.append(fullDeckPath)

        # Create decks
        for deck in newDeckPaths:
            self.connector.createDeck(deck)

    def _getFullDeckPath(self, deckName):
        if self.defaultDeck == None:
            return deckName
        else:
            return self.defaultDeck + "::" + deckName

    def _checkForDefaultDeck(self):
        self.currentDecks = self.connector.getDeckNames()
        if self.defaultDeck not in self.currentDecks:
            self.connector.createDeck(self.defaultDeck)

    def buildAnkiNotes(self, ankiQuestions): # [AnkiQuestion]

        notes = []
        for i in ankiQuestions:
            notes.append(self.AnkiNoteBuilder.buildNote(i))

        finalNotes = {}
        finalNotes["notes"] = notes
        return finalNotes

