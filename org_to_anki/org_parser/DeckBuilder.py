
from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from ..ankiClasses.AnkiQuestionFactory import AnkiQuestionFactory
from . import DeckBuilderUtils
from . import ParserUtils

import os


class DeckBuilder:

    utils = DeckBuilderUtils.DeckBuilderUtils()

    def buildDeck(self, questions: [str], deckName: str, filePath: str, fileType: str='basic'):

        # TODO: Remove lower
        if fileType.lower() == 'basic':
            deck = self._buildNewDeck(questions, deckName, filePath)
        elif fileType.lower() == 'topics':
            deck = self._buildTopics(questions, deckName, filePath)
        elif fileType.lower() == 'flattopics':
            deck = self._buildFlatTopics(questions, deckName, filePath)
        elif fileType.lower() == 'organisedflatfile':
            deck = self._buildOrganisedFlatFile(questions, deckName, filePath)
        elif fileType.lower() == 'organisedfile':
            deck = self._buildOrganisedFile(questions, deckName, filePath)
        else:
            raise Exception('Unsupported file type: ' + fileType)

        return deck

    def _buildTopics(self, questions, deckName, filePath):

        deck = AnkiDeck(deckName)

        subSections = self._sortTopicsSubDeck(questions)

        for section in subSections:
            subDeckName = section.pop(0).replace("*", "").strip()
            subDeck = self._buildNewDeck(section, subDeckName, filePath, 2, 3)
            deck.addSubdeck(subDeck)

        return deck

    def _buildFlatTopics(self, questions, deckName, filePath):

        subSections = self._sortTopicsSubDeck(questions)

        if (self.utils.countAsterisk(subSections[0][0]) != 1):
            raise Exception('Topics file is not correctly formatted')

        allQuestion = []
        for i in subSections:
            allQuestion.extend(i)

        formattedQuestions = []
        currentTopic = questions.pop(0).replace("*", "")
        while len(questions) > 0:
            q = questions.pop(0)
            if (self.utils.countAsterisk(q) == 1):
                currentTopic = q.replace("*", "")
            elif (self.utils.countAsterisk(q) == 2):
                q = q.replace("*", "")
                q = "** " + currentTopic + "\n" + q
                formattedQuestions.append(q)
            else:
                formattedQuestions.append(q)

        deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 2, 3)
        return deck

    def _buildOrganisedFile(self, questions, deckName, filePath):

        subSections = self._sortTopicsSubDeck(questions)

        formattedQuestions = []

        for section in subSections:
            for q in section:
                if (self.utils.countAsterisk(q) == 1):
                    continue
                else:
                    formattedQuestions.append(q)
        
        deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 2, 3)
        return deck

    def _buildOrganisedFlatFile(self, questions, deckName, filePath):

        subSections = self._sortTopicsSubDeck(questions)

        formattedQuestions = []
        for section in subSections:
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

        # for i in formattedQuestions:
        #     print(i)
        deck = self._buildNewDeck(formattedQuestions, deckName, filePath, 3, 4)
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
                raise Exception("Issue parsing topics deck.")

        subSections.append(currentSection[:])

        return subSections

    def _buildNewDeck(self, questions, deckName, filePath, questionLine=1, answerLine=2):

        deck = AnkiDeck(deckName)
        # Get deck comments
        while questions[0].strip()[0] == "#":
            comment = questions.pop(0)
            deck.addComment(comment)
            parameters = ParserUtils.convertLineToParameters(comment)
            for key in parameters.keys():
                deck.addParameter(key, parameters.get(key))

        # Answer are indented by a single or more Asterisks
        numberOfQuestionAsterisk = questionLine
        numberOfAnswerAsterisk = answerLine
        questionFactory = AnkiQuestionFactory(deckName, filePath)

        while len(questions) > 0:
            line = questions.pop(0)
            noAsterisk = self.utils.countAsterisk(line)
            if len(line) == 0:
                continue

            # Question line
            if noAsterisk == numberOfQuestionAsterisk:
                # Allow for multi line questions
                # If new question => generate ankiQuestion and start new
                if questionFactory.questionHasAnswers() == True:
                    newQuestion = questionFactory.buildQuestion()
                    if (newQuestion.getParameter("type") != 'notes'):
                        deck.addQuestion(newQuestion)
                    questionFactory.addQuestionLine(line)
                else:
                    questionFactory.addQuestionLine(line)

            # Answer line
            elif noAsterisk > numberOfQuestionAsterisk:
                questionFactory.addAnswerLine(line) ### No subquestion line => logic should be moved when answers are built ###

            # Comment line
            elif line.strip()[0] == "#":
                # Now comments are for deck and not for question
                questionFactory.addCommentLine(line)

            else:
                print("Current line is not recognised: " + line)
        
        # Add last question
        if questionFactory.questionHasAnswers():
            newQuestion = questionFactory.buildQuestion()
            if (newQuestion.getParameter("type") != 'notes'):
                deck.addQuestion(newQuestion)

        return deck