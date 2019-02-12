# parse data into expected format
from ..ankiClasses.AnkiDeck import AnkiDeck
from .DeckBuilder import DeckBuilder
from ..converters.BulletPointHtmlConverter import convertBulletPointsDocument
from . import ParserUtils


def parse(filePath): # (filePath: str): -> ([AnkiDeck]):

    deckBuilder = DeckBuilder()

    # Validate data
    fileExtension = filePath.split(".")[-1] # Unhandled index error here
    if (fileExtension == "org" or fileExtension == "txt"):
        data = _formatFile(filePath)
    # 
    elif ((fileExtension == "html") or (fileExtension == "htm")):
        formatedData = convertBulletPointsDocument(filePath)
        data = formatedData.split("\n")
    else:
        raise Exception("Inccorrect file format given")
    fileName = filePath.split("/")[-1].split(".")[0]

    comments, content = _sortData(data)

    globalParameters = ParserUtils.convertCommentsToParameters(comments)
    fileType = globalParameters.get("fileType", "basic")

    deck = deckBuilder.buildDeck(content, fileName, filePath, fileType)

    # TODO refactor this section into DeckBuilder
    for key in globalParameters:
        deck.addParameter(key, globalParameters[key])
    for comment in comments:
        deck.addComment(comment)

    return deck


def _formatFile(filePath):# (filePath: str):

    with open(filePath, 'r') as file:
        data = file.read().split('\n')

    return data


def _sortData(rawFileData): #(rawFileData: [str]) -> ([str], [str]):

    comments, questions = [], []

    questionsSection = False
    for i in range(0, len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem.strip()[0]
            if firstLetter == "#" and questionsSection is False:
                comments.append(currentItem)
            elif firstLetter == "*" or questionsSection:
                questionsSection = True
                questions.append(currentItem)

    return (comments, questions)
