# Using AnkiConnect project as a sub-module import and use AnkiBridge 
import sys
# sys.path.insert(0, "org_to_anki/anki-connect/AnkiConnect.py")
import os
dirname = os.path.dirname(__file__)
ankiConnectPath = os.path.join(dirname, "../anki-connect/AnkiConnect.py")
sys.path.append(ankiConnectPath)

from .. import config

# Anki imports
try:
    from AnkiConnect import AnkiConnect
    import anki
    import aqt
    from aqt.utils import showInfo
except:
    pass
class AnkiPluginConnector:

    # TODO => integrate for anki
    def __init__(self):
        try: 
            self.AnkiBridge = AnkiConnect()
        except:
            self.AnkiBridge = None
        print(ankiConnectPath)
        self.defaultDeck = config.defaultDeck

    def uploadNewDeck(self, deck): # AnkiDeck

        ### Upload deck to Anki in embedded mode ###
        # showInfo("Creating deck")
        # showInfo(str(sys.version))
        # # showInfo(print(deck))
        # showInfo(str(deck.getDeckNames()))
        # print(sys.version)


        # # Create deck if it does not exist for main deck
        # self.AnkiBridge.createDeck("New test Deck")


        # Ensure subdecks also exist

        # Add notes

        # Add media 

        self._checkForDefaultDeck()
        self._buildNewDecksAsRequired(deck.getDeckNames())
        # Build new questions
        notes = self.buildIndividualAnkiNotes(deck.getQuestions())
        media = self.prepareMedia(deck.getMedia())

        # TODO Get all question from that deck and
        # use this to verify questions need to be uploaded
        # self._removeAlreadyExistingQuestions()

        # Insert new question through the api
        # TODO fix both of these
        # self.AnkiBridge.uploadNotes(notes)

        # showInfo(str(notes))
        for note in notes:
            self.AnkiBridge.addNote(note)

        # self.AnkiBridge.uploadMediaCollection(media)
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
            notes.append(self._buildNote(i))

        finalNotes = {}
        finalNotes["notes"] = notes
        return finalNotes
    
    def buildIndividualAnkiNotes(self, ankiQuestions):

        allNotes = []
        for i in ankiQuestions:
            # singleNote = {}
            # singleNote["notes"] = self._buildNote(i)
            allNotes.append(self._buildNote(i))
        
        return allNotes

    def _buildNote(self, ankiQuestion): # AnkiQuestion

        # All decks stored under default deck
        if ankiQuestion.deckName == "" or ankiQuestion.deckName is None:
            # TODO log note was built on default deck
            deckName = self.defaultDeck
        else:
            deckName = self._getFullDeckPath(ankiQuestion.deckName)

        # TODO: Verify model name correctly and use parameters
        if ankiQuestion.getParameter("type") is not None:
            modelName = ankiQuestion.getParameter("type")
        else:
            modelName = "Basic"

        note = {"deckName": deckName, "modelName": modelName}
        note["tags"] = ankiQuestion.getTags()

        # Generate fields
        fields = {}
        fields["Front"] = self._createQuestionString(ankiQuestion.getQuestions())
        fields["Back"] = self._createAnswerString(ankiQuestion.getAnswers())

        note["fields"] = fields
        return note

    def _createQuestionString(self, questions): #([str])

        if len(questions) == 1:
            question =  questions[0].replace("\n", "<br>")
            return question
        else:
            questionString = ""
            for q in questions:
                q = q.strip().replace("\n", "<br>")
                questionString += q + " <br>"
            return questionString
            

    def _createAnswerString(self, answers, bulletPoints=True): # ([str], bool)

        result = ""
        if not bulletPoints:
            for i in answers:
                result += i + "<br>"  # HTML link break
        else:
            # Can only can create single level of indentation. Align
            # bulletpoints.
            result += "<ul style='list-style-position: inside;'>"
            for i in answers:
                if isinstance(i, str):
                    result += "<li>" + i + "</li>"
                elif isinstance(i, list):
                    result += self._createAnswerString(i)
                else:
                    # showInfo(str(type(i)))
                    raise Exception("Unsupported action with answer string from => ") # + str(i))

            result += "</ul>"
        return result
