import sys, os
import base64
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses.AnkiQuestionMedia import AnkiQuestionMedia
from org_to_anki.ankiConnectWrapper.AnkiConnector import AnkiConnector

def testImageTagCorrectProccesed():

    filename = "tests/testData/image.org"
    actualDeck = parseData.parse(os.path.abspath(filename))

    imageFile = "tests/testData/imageFolder/image.png"
    fullImagePath = os.path.abspath(imageFile)

    with open(fullImagePath, 'rb') as data:
        mediaItem = AnkiQuestionMedia("image", "image.png", data.read())

    assert(actualDeck.getQuestions()[0].getAnswers()[1] == '<img src="image.png" />')
    assert(mediaItem == actualDeck.getMedia()[0])

def testImageCorrectlyUploaded():

    filename = "tests/testData/image.org"
    actualDeck = parseData.parse(os.path.abspath(filename))

    imageFile = "tests/testData/imageFolder/image.png"
    fullImagePath = os.path.abspath(imageFile)

    a = AnkiConnector()
    preparedMedia = a.prepareMedia(actualDeck.getMedia())
    assert(preparedMedia[0].get('fileName') == "image.png")

    with open(fullImagePath, 'rb') as data:
        encodedImage = base64.b64encode(data.read()).decode("utf-8")
    assert(preparedMedia[0].get("data") == encodedImage)

def testImageWithSize():

    filename = "tests/testData/image.org"
    actualDeck = parseData.parse(os.path.abspath(filename))

    assert(actualDeck.getQuestions()[2].getAnswers()[0] == '<img src="image.png" style="width:100px;height:100px;" />')