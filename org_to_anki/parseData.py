# parse data into expected format
import os

from . import AnkiQuestion


def parse(filePath):

    file = open(filePath, "r")
    data = file.read().split('\n')
    fileName = filePath.split("/")[-1].split(".")[0]

    comments, questions, badFormatting = _sortData(data)
    # TODO bad formatting should be correctly logged

    questions = _buildQuestions(questions, fileName)

    return questions


def _buildQuestions(questions, deckName):

    # TODO identify file type from comments or assume is basic
    # Build properites file
    # File identifer
    questionLine = 1
    answerLine = 2
    orgType = "basic"

    formatedQuestions = []
    currentQuestion = None

    for line in questions:
        noAstrics = line.split(' ')[0].count('*', 0, 10)
        # TODO lines of differnt type need different formatting
        line = _formatLine(line)

        if noAstrics == questionLine:
            # Store old question
            if currentQuestion != None:
                formatedQuestions.append(currentQuestion)
            # Next Question
            currentQuestion = AnkiQuestion.AnkiQuestion(line, deckName)
        elif noAstrics == answerLine:
            currentQuestion.addAnswer(line)

    if currentQuestion != None:
        formatedQuestions.append(currentQuestion)
        currentQuestion = None

    return formatedQuestions


def _formatLine(line):

    line = " ".join(line.split(" ")[1:])  # Remove leading astrics
    line = line.capitalize()
    line = line.strip()

    return line


def _sortData(rawFileData):

    comments = []
    questions = []
    badFormatting = []

    for i in range(0, len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem[0]
            if firstLetter == "#":
                comments.append(currentItem)
            elif firstLetter == "*":
                questions.append(currentItem)
            else:
                badFormatting.append(
                    ["Line starts incorrectly at line no " + i, currentItem])

    return (comments, questions, badFormatting)


if __name__ == "__main__":

    dir = os.path.dirname(__file__)
    filePath = os.path.join(dir, '../tests/testData/basic.org')
    questions = parse(filePath)
    print(questions[0])
