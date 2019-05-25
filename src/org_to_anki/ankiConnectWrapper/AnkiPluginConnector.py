# Using AnkiConnect project as a sub-module import and use AnkiBridge 
import sys
# sys.path.insert(0, "org_to_anki/anki-connect/AnkiConnect.py")
import os
# TODO => need to embbeded the AnkiConnectCode
# dirname = os.path.dirname(__file__)
# ankiConnectPath = os.path.join(dirname, "../anki-connect/AnkiConnect.py")
# sys.path.append(ankiConnectPath)

from .. import config
from .AnkiBridge import AnkiBridge
from .AnkiNoteBuilder import AnkiNoteBuilder

# Anki imports
try:
    import anki
    import aqt
    from aqt.utils import showInfo
except:
    pass
class AnkiPluginConnector:

    def __init__(self):
        self.AnkiBridge = AnkiBridge()
        self.defaultDeck = config.defaultDeck
        self.AnkiNoteBuilder = AnkiNoteBuilder()

    def uploadNewDeck(self, deck): # AnkiDeck

        ### Upload deck to Anki in embedded mode ###
        self._checkForDefaultDeck()
        self._buildNewDecksAsRequired(deck.getDeckNames())
        # Build new questions
        notes = self.buildIndividualAnkiNotes(deck.getQuestions())
        media = self.prepareMedia(deck.getMedia())

        # Add notes => TODO => needs to handle exception better
        numberOfDuplicateNotes = 0
        for note in notes:
            try:
                self.AnkiBridge.addNote(note)
            except Exception as e:
                if str(e) == "cannot create note because it is a duplicate":
                    numberOfDuplicateNotes += 1
                else:
                    raise e

        # Add Media => TODO => not tested
        for i in media:
            self.AnkiBridge.storeMediaFile(i.get("fileName"), i.get("data"))


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
            self.AnkiBridge.createDeck(deck)

    def _getFullDeckPath(self, deckName): # (str)
        return str(self.defaultDeck + "::" + deckName)

    def _checkForDefaultDeck(self):
        self.currentDecks = self.AnkiBridge.deckNames()
        if self.defaultDeck not in self.currentDecks:
            self.AnkiBridge.createDeck(self.defaultDeck)

    # TODO => refactor
    def buildAnkiNotes(self, ankiQuestions): # [AnkiQuestion]

        notes = []
        for i in ankiQuestions:
            notes.append(self.AnkiNoteBuilder.buildNote(i))

        finalNotes = {}
        finalNotes["notes"] = notes
        return finalNotes
    
    def buildIndividualAnkiNotes(self, ankiQuestions):

        allNotes = []
        for i in ankiQuestions:
            allNotes.append(self.AnkiNoteBuilder.buildNote(i))
        
        return allNotes

    ### These methods are still in beta and are subject to change ###

    # Get deck Notes
    def getDeckNotes(self, deckName):
        # TODO => revisit return type
        return self.AnkiBridge.getDeckNotes(deckName)

    # Add new notes
    def addNote(self, note):
        # TODO need to verify this note is logically correct
        if isinstance(note, list) == False:
            note = [note]

        builtNotes = self.buildIndividualAnkiNotes(note)
        for note in builtNotes:
            self.AnkiBridge.addNote(note)

    # Delete notes
    def deleteNotes(self, noteIds):
        # TODO ensure that noteID is an array
        self.AnkiBridge.deleteNotes(noteIds)

    # Update Note fields
    def updateNoteFields(self, note):

        # TODO ensure note is logically correct
        self.AnkiBridge.updateNoteFields(note)

    def getConfig(self):
        return aqt.mw.addonManager.getConfig(__name__)
        
    def writeConfig(self, config):
        aqt.mw.addonManager.writeConfig(__name__, config)
