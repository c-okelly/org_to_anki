# parse data into expected format
import os

from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck


def parse(filePath:str) -> ([AnkiDeck]):

    data = _formatFile(filePath)
    fileName = filePath.split("/")[-1].split(".")[0]

    comments, content, badFormatting = _sortData(data)
    # TODO bad formatting should be correctly logged

    globalParameters = _convertCommentsToParameters(comments)
    fileType = globalParameters.get("fileType", "basic")

    deck = _buildQuestions(content, fileName, fileType)

    return deck

def _formatFile(filePath:str):

    file = open(filePath, "r")
    data = file.read().split('\n')

    return data


def _convertCommentsToParameters(comments:[str]):

    parameters = {}
    for line in comments:
        line = line.strip()[line.count("#"):]
        pairs = line.split(",")
        for item in pairs:
            if "=" in item:
                item = item.strip()
                parts = item.split("=")
                parameters[parts[0]] = parts[1]

    return parameters


def _buildQuestions(questions:[str], deckName:str, fileType:str='basic'):

    questionLine = 1
    answerLine = 2

    deck = AnkiDeck(deckName)

    currentQuestion = None

    for line in questions:
        noAstrics = line.split(' ')[0].count('*', 0, 10)
        # TODO lines of differnt type need different formatting

        if noAstrics == questionLine:
            line = " ".join(line.split(" ")[1:])
            # Store old question
            if currentQuestion != None:
                deck.addQuestion(currentQuestion)
            # Next Question
            currentQuestion = AnkiQuestion(line, deckName)

        elif noAstrics == answerLine:
            line = " ".join(line.split(" ")[1:])
            currentQuestion.addAnswer(line)

        elif noAstrics > answerLine:
            #Remove answer astrics
            line = line.strip().split(" ")
            line[0] = line[0][answerLine:]
            line = " ".join(line)
            currentQuestion.addAnswer(line)
            
        else:
            raise Exception("Line incorrectly processed.")

    if currentQuestion != None:
        deck.addQuestion(currentQuestion)
        currentQuestion = None

    return deck 


def _formatLine(line:str) -> (str):

    line = line.capitalize()
    line = line.strip()

    return line


def _sortData(rawFileData:[str]) -> ([str], [str], [str]):

    comments, questions, badFormatting = [], [], []

    for i in range(0, len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem.strip()[0]
            if firstLetter == "#":
                comments.append(currentItem)
            elif firstLetter == "*":
                questions.append(currentItem)
            else:
                badFormatting.append(
                    ["Line starts incorrectly at line no " + str(i) + ". " + currentItem])

    return (comments, questions, badFormatting)


if __name__ == "__main__":

    # dir = os.path.dirname(__file__)
    # filePath = os.path.join(dir, '../tests/testData/basic.org')
    # questions = parse(filePath)
    # print(questions[0])

    x = _convertCommentsToParameters(["#fileType=basic, secondArg=10", "##file=basic"])
    print(x)
