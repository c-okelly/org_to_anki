
from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from ..ankiClasses.AnkiQuestionFactory import AnkiQuestionFactory
from . import DeckBuilderUtils
from . import ParserUtils

import os


class DeckBuilder:

    utils = DeckBuilderUtils.DeckBuilderUtils()

    def buildDeck(self, questions: [str], deckName: str, filePath: str, fileType: str='basic'):

        if fileType == 'basic':
            deck = self._buildNewDeck(questions, deckName, filePath)
        elif fileType == 'topics':
            deck = self._buildTopics(questions, deckName, filePath)
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

    def _sortTopicsSubDeck(self, questions):

        subSections = []
        currentSection = []

        for line in questions:
            # first line
            noAstrics = line.split(' ')[0].count('*', 0, 10)
            if noAstrics == 1:
                if len(currentSection) > 0:
                    subDeck = currentSection[:]
                    currentSection = []
                    subSections.append(subDeck)
                currentSection.append(line)
            elif noAstrics > 1 or line.strip()[0] == "#":
                currentSection.append(line)
            else:
                raise Exception("Issue parsing topics deck.")

        subSections.append(currentSection[:])

        return subSections

    def _buildNewDeck1(self, deck, questions, numberQuestionAsterisk = 1):

        # Answer are indented by a single or more Asterisks
        numberAnswerAsterisk = 2
        questionFactory = AnkiQuestionFactory()

        while len(questions) > 0:
            line = questions.pop(0)
            noAstrics = self.utils.countAstrics(line)

            # Question line
            if noAstrics == numberQuestionAsterisk:
                # Allow for multi line questions
                # If new question => generate ankiQuestion and start new
                if questionFactory.questionHasAnswers() == True:
                    deck.addQuestion(questionFactory.buildQuesiton())
                else:
                    questionFactory.addQuestionLine(line)
                pass

            # Answer line
            elif noAstrics > numberQuestionAsterisk:
                questionFactory.addAnswerLine(line) ### No subqestion line => logic should be moved when answers are built ###

            # Comment line
            else:
                questionFactory.addCommentLine(line)
        
        # Add last question
        if questionFactory.questionHasAnswers():
            deck.addQuestion(questionFactory.buildQuesiton())

    def _buildNewDeck(self, questions, deckName, filePath, questionLine=1, answerLine=2):

        deck = AnkiDeck(deckName)
        currentQuestion = None

        while len(questions) > 0:
            line = questions.pop(0)
            noAstrics = self.utils.countAstrics(line)

            # Question line
            if noAstrics == questionLine:
                line = self.utils.removeAstrics(line)
                # Store old question
                if currentQuestion is not None: ### TODO Check for anwers with no questions?? and len(currentQuestion.getAnswers()) != 0:
                    deck.addQuestion(currentQuestion)
                # Next Question
                currentQuestion = AnkiQuestion(line)

            # Asnwer line
            elif noAstrics == answerLine:
                line = self.utils.removeAstrics(line)
                line = self.utils.parseAnswerLine(line, filePath, deck)
                currentQuestion.addAnswer(line)

            # Sublist in question
            elif noAstrics > answerLine:

                subList = []
                subList.append(line)

                while len(questions) > 0 and self.utils.countAstrics(
                        questions[0]) > answerLine:
                    line = questions.pop(0)
                    line = self.utils.parseAnswerLine(line, filePath, deck)
                    subList.append(line)

                formatedSubList = self.utils.generateSublist(subList)
                currentQuestion.addAnswer(formatedSubList)

            elif noAstrics == 0 and line[0] == "#":
                # Deck questions
                if currentQuestion is None:
                    deck.addComment(line)
                    params = ParserUtils.convertLineToParamters(line)
                    for key in params.keys():
                        deck.addParameter(key, params[key])
                else:
                    currentQuestion.addComment(line)
                    parameters = ParserUtils.convertLineToParamters(line)
                    for key in parameters.keys():
                        currentQuestion.addParameter(key, parameters.get(key))

            else:
                raise Exception("Line incorrectly processed.")

        # Add last question
        if currentQuestion is not None:
            deck.addQuestion(currentQuestion)
            currentQuestion = None

        return deck
