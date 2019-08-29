
from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from ..ankiClasses.AnkiQuestionFactory import AnkiQuestionFactory
from . import DeckBuilderUtils
from . import ParserUtils

import os


class DeckBuilder:

    utils = DeckBuilderUtils.DeckBuilderUtils()

    def buildDeck(self, data, deckName, filePath, fileType ='basic'): # ([str], str, str, str)

        deck = AnkiDeck(deckName)

        comments, questions = self._sortData(data)
        globalParameters = ParserUtils.convertCommentsToParameters(comments)

        # Add global params to deck
        for key in globalParameters:
            if self._checkValidGlobalParameter(key, globalParameters[key]):
                deck.addParameter(key, globalParameters[key])
        for comment in comments:
            deck.addComment(comment)

        fileType = globalParameters.get("fileType", "basic")

        # TODO: Remove lower
        if fileType.lower() == 'basic':
            deck = self._buildNewDeck(questions, deckName, filePath, currentDeck=deck)
        elif fileType.lower() == 'topics':
            deck = self._buildTopics(questions, deckName, filePath, deck)
        elif fileType.lower() == 'flattopics':
            deck = self._buildFlatTopics(questions, deckName, filePath, deck)
        elif fileType.lower() == 'organisedflatfile':
            deck = self._buildOrganisedFlatFile(questions, deckName, filePath, deck)
        elif fileType.lower() == 'organisedfile':
            deck = self._buildOrganisedFile(questions, deckName, filePath, deck)
        else:
            raise Exception('Unsupported file type: ' + fileType)


        return deck

    def _buildTopics(self, questions, deckName, filePath, deck):

        subSections = self._sortTopicsSubDeck(questions)

        for section in subSections:
            subDeckName = section.pop(0).replace("*", "").strip()
            subDeck = self._buildNewDeck(section, subDeckName, filePath, 2, 3)
            deck.addSubdeck(subDeck)

        return deck

    def _buildFlatTopics(self, questions, deckName, filePath, deck):

        subSections = self._sortTopicsSubDeck(questions)

        if (self.utils.countAsterisk(subSections[0][0]) != 1):
            raise Exception('Topics file is not correctly formatted')

        for section in subSections:
            formattedQuestions = []

            currentTopic = questions.pop(0).replace("*", "")
            while len(section) > 0:
                q = section.pop(0)
                if (self.utils.countAsterisk(q) == 1):
                    currentTopic = q.replace("*", "")
                elif (self.utils.countAsterisk(q) == 2):
                    q = q.replace("*", "")
                    q = "** " + currentTopic + "\n" + q
                    formattedQuestions.append(q)
                else:
                    formattedQuestions.append(q)
            deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 2, 3, deck)

        return deck

    def _buildOrganisedFile(self, questions, deckName, filePath, deck):

        subSections = self._sortTopicsSubDeck(questions)

        for section in subSections:
            formattedQuestions = []
            for q in section:
                if (self.utils.countAsterisk(q) == 1):
                    continue
                else:
                    formattedQuestions.append(q)
            deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 2, 3, deck)
        
        return deck

    def _buildOrganisedFlatFile(self, questions, deckName, filePath, deck):

        subSections = self._sortTopicsSubDeck(questions)

        for section in subSections:

            formattedQuestions = []
            currentTopic = section.pop(0).replace("*", "")

            while len(section) > 0:
                q = section.pop(0)
                if (self.utils.countAsterisk(q) == 2):
                    # Ignore line on second level of indent as only used for organization
                    continue
                elif (self.utils.countAsterisk(q) == 3):
                    q = q.replace("*", "")
                    q = "*** " + currentTopic + "\n" + q
                    formattedQuestions.append(q)
                else:
                    formattedQuestions.append(q)
            deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 3, 4, deck)

        return deck

    def _sortTopicsSubDeck(self, questions):

        subSections = []
        currentSection = []

        for line in questions:
            # first line
            noAsterisk =self.utils.countAsterisk(line)
            if noAsterisk == 1:
                if len(currentSection) > 0:
                    subDeck = currentSection[:]
                    currentSection = []
                    subSections.append(subDeck)
                currentSection.append(line)
            elif noAsterisk > 1 or line.strip()[0] == "#":
                currentSection.append(line)
            else:
                currentSection.append(line)

        subSections.append(currentSection[:])

        return subSections

    def _buildNewDeck(self, questions, deckName, filePath, questionLine=1, answerLine=2, currentDeck=None):

        if currentDeck == None:
            deck = AnkiDeck(deckName)
        else:
            deck = currentDeck

        if len(questions) == 0:
            return deck

        # Get current metadata 
        sectionMetadata = {}

        # Get section comments
        while questions[0].strip()[0] == "#":
            parameters = ParserUtils.convertLineToParameters(questions.pop(0))
            for key in parameters.keys():
                sectionMetadata[key] = parameters.get(key)

        # Answer are indented by a single or more Asterisks
        numberOfQuestionAsterisk = questionLine
        numberOfAnswerAsterisk = answerLine
        questionFactory = AnkiQuestionFactory(deckName, filePath)

        # Add metadata for section to new Question
        for key in sectionMetadata: # This is a bit lazy
            questionFactory.addCommentLine("# {} = {}".format(key, sectionMetadata[key]))

        questionMetadata = {}
        while len(questions) > 0:
            line = questions.pop(0)
            noAsterisk = self.utils.countAsterisk(line)
            if len(line) == 0:
                continue

            # Question line
            if noAsterisk == numberOfQuestionAsterisk:
                # Allow for multi line questions
                # If new question line and question is already valid 
                # => generate ankiQuestion and start new
                if questionFactory.isValidQuestion():
                    questionMetadata = {} # Clear questionMetadata

                    newQuestion = questionFactory.buildQuestion() # Possibly include sectionMetadata here?
                    if (newQuestion.getParameter("type") != 'notes'):
                        deck.addQuestion(newQuestion)
                    # Add metadata for section to new Question
                    for key in sectionMetadata: # This is a bit lazy
                        questionFactory.addCommentLine("# {} = {}".format(key, sectionMetadata[key]))

                    questionFactory.addQuestionLine(line)
                else:
                    questionFactory.addQuestionLine(line)

            # Answer line
            elif noAsterisk > numberOfQuestionAsterisk:
                questionFactory.addAnswerLine(line, questionMetadata) ### No subquestion line => logic should be moved when answers are built ###

            # Comment line
            elif line.strip()[0] == "#":
                # Now comments are for deck and not for question
                questionFactory.addCommentLine(line)
                # Parse comment for parameters and add to questionMetadata
                parameters = ParserUtils.convertLineToParameters(line)
                for key in parameters.keys():
                    questionMetadata[key] = parameters.get(key)

            # Code line
            elif line.strip().startswith("```"):
                codeSection = []
                line = line.strip()
                language = None
                if len(line) > 3:
                    language = line[3:]
                while len(questions) > 0:
                    codeLine = questions.pop(0)
                    if codeLine.startswith("```"):
                        break
                    else:
                        codeSection.append(codeLine)
                questionFactory.addCode(language, codeSection) 
            else:
                print("Current line is not recognised: " + line)
        
        # Add last question
        if questionFactory.isValidQuestion():
            # TODO take meta stuff into account
            newQuestion = questionFactory.buildQuestion()  # Possibly include sectionMetadata here?
            if (newQuestion.getParameter("type") != 'notes'):
                deck.addQuestion(newQuestion)

        return deck

    def _checkValidGlobalParameter(self, key, value):

        # Number of key types are not supported at the section level
        if (key != "type" or key != "noteType") and value == "Cloze":
            return False 
        else:
            return True 

    def _sortData(self, rawFileData): #(rawFileData: [str]) -> ([str], [str]):

        comments, questions = [], []

        questionsSection = False
        for i in range(0, len(rawFileData)):
            currentItem = rawFileData[i]
            if len(currentItem.strip()) > 0:
                firstLetter = currentItem.strip()[0]
                # Check if line is empty
                if (len(currentItem.replace("*", "").strip()) == 0 or len(currentItem.replace("#", "").strip()) == 0):
                    continue
                if firstLetter == "#" and questionsSection is False:
                    comments.append(currentItem)
                elif firstLetter == "*" or questionsSection:
                    questionsSection = True
                    questions.append(currentItem)

        return (comments, questions)
