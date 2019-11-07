# parse data into expected format
from ..ankiClasses.AnkiDeck import AnkiDeck
from .DeckBuilder import DeckBuilder
from ..converters.BulletPointHtmlConverter import convertBulletPointsDocument
from . import ParserUtils

def parse(filePath): # (filePath: str): -> ([AnkiDeck]):


    data = _loadFile(filePath)

    return _buildDeck(data, filePath)

# TODO test properly

def buildNamedDeck(orgList, deckName):

    deckBuilder = DeckBuilder()
    deck = deckBuilder.buildDeck(orgList, deckName, "onlyData")
    return deck

def _buildDeck(data, filePath):

    deckBuilder = DeckBuilder()
    fileName = filePath.split("/")[-1].split(".")[0]

    deck = deckBuilder.buildDeck(data, fileName, filePath)
    
    return deck

def _loadFile(filePath):

    # Validate data
    fileExtension = filePath.split(".")[-1] # Unhandled index error here
    if (fileExtension == "org" or fileExtension == "txt"):
        data = _formatFile(filePath)
    elif ((fileExtension == "html") or (fileExtension == "htm")):
        formatedData = convertBulletPointsDocument(filePath)
        data = formatedData.split("\n")
    else:
        raise TypeError("Inccorrect file format given")
    
    return data



def _formatFile(filePath):# (filePath: str):

    with open(filePath, mode="r", encoding="utf-8") as file:
        data = file.read().split('\n')

    return data


