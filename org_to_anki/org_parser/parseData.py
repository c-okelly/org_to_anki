# parse data into expected format
from ..ankiClasses.AnkiDeck import AnkiDeck
from .DeckBuilder import DeckBuilder


def parse(filePath: str) -> ([AnkiDeck]):

    deckBuilder = DeckBuilder()

    data = _formatFile(filePath)
    fileName = filePath.split("/")[-1].split(".")[0]

    comments, content = _sortData(data)

    globalParameters = convertCommentsToParameters(comments)
    fileType = globalParameters.get("fileType", "basic")

    deck = deckBuilder.buildDeck(content, fileName, fileType)

    # TODO refactor this section into DeckBuilder
    for key in globalParameters:
        deck.addParameter(key, globalParameters[key])
    for comment in comments:
        deck.addComment(comment)

    return deck


def _formatFile(filePath: str):

    file = open(filePath, "r")
    data = file.read().split('\n')

    return data


def convertCommentsToParameters(comments: [str]):

    parameters = {}
    for line in comments:
        parameters.update(convertLineToParamters(line))

    return parameters

def convertLineToParamters(line: str):

    parameters = {}
    line = line.strip()[line.count("#"):]
    pairs = line.split(",")
    for item in pairs:
        if "=" in item:
            item = item.strip()
            parts = item.split("=")
            parameters[parts[0].strip()] = parts[1].strip()

    return parameters



def _sortData(rawFileData: [str]) -> ([str], [str], [str]):

    comments, questions = [], []

    questionsSection = False
    for i in range(0, len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem.strip()[0]
            if firstLetter == "#" and questionsSection == False:
                comments.append(currentItem)
            elif firstLetter == "*" or questionsSection == True:
                questionsSection = True
                questions.append(currentItem)

    return (comments, questions)