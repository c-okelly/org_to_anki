
from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck
from . import ParserUtils

import os


class DeckBuilder:

    def buildDeck(self, questions: [str], deckName: str, filePath: str, fileType: str='basic'):

        if fileType == 'basic':
            deck = self._buildBasic(questions, deckName, filePath)
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
            subDeck = self._buildBasic(section, subDeckName, filePath, 2, 3)
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

    def _removeAstrics(self, line: str):

        line = line.strip().split(" ")[1:]
        line = " ".join(line)

        return line

    def _countAstrics(self, line: str):

        return line.split(' ')[0].count('*', 0, 10)

    def _generateSublist(self, subItems: [str]):

        formatedList = []

        indentaionLevel = self._countAstrics(subItems[0])
        for item in subItems:
            if self._countAstrics(item) == indentaionLevel:
                formatedList.append(item)
            elif self._countAstrics(item) > indentaionLevel and isinstance(formatedList[-1], list):
                formatedList[-1].append(item)
            else:
                formatedList.append([item])

        cleaned = []
        for i in formatedList:
            if isinstance(i, list):
                cleaned.append(self._generateSublist(i))
            else:
                cleaned.append(self._removeAstrics(i))

        return cleaned


    def _parseAnswerLine(self, answerLine: str, filePath: str, currentDeck: AnkiDeck):

        # Check if line needs to be parsed
        if "[" in answerLine and "]" in answerLine:
            # print(answerLine)
            # print(filePath)
            if "http://" in answerLine or "www." in answerLine:
                raise Exception("Line could not be parsed: " + answerLine)

            elif answerLine.count("[") == 1:
                relativeImagePath = answerLine.split("[")[1].split("]")[0]
                fileName = os.path.basename(relativeImagePath)
                baseDirectory = os.path.dirname(filePath) 
                imagePath = os.path.join(baseDirectory, relativeImagePath)

                if len(relativeImagePath) > 0 and os.path.exists(imagePath):

                    currentDeck.addImage(fileName, imagePath)
                    answerLine = '<img src="' + os.path.basename(imagePath) + '" />'
                else:
                    print("Could not find image on line:", answerLine)

            else:
                raise Exception("Line could not be parsed: " + answerLine)
        
        return answerLine

    def _buildBasic(self, questions, deckName, filePath, questionLine=1, answerLine=2):

        deck = AnkiDeck(deckName)
        currentQuestion = None

        while len(questions) > 0:
            line = questions.pop(0)
            noAstrics = self._countAstrics(line)
            # TODO lines of differnt type need different formatting

            if noAstrics == questionLine:
                line = self._removeAstrics(line)
                # Store old question
                if currentQuestion is not None:
                    deck.addQuestion(currentQuestion)
                # Next Question
                currentQuestion = AnkiQuestion(line)

            elif noAstrics == answerLine:
                line = self._removeAstrics(line)
                line = self._parseAnswerLine(line, filePath, deck)
                currentQuestion.addAnswer(line)

            # Sublist in question
            elif noAstrics > answerLine:

                subList = []
                subList.append(line)

                while len(questions) > 0 and self._countAstrics(
                        questions[0]) > answerLine:
                    line = questions.pop(0)
                    line = self._parseAnswerLine(line, filePath, deck)
                    subList.append(line)

                formatedSubList = self._generateSublist(subList)
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

        if currentQuestion is not None:
            deck.addQuestion(currentQuestion)
            currentQuestion = None

        return deck
