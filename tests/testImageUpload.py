import sys, os
import base64
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses.AnkiQuestionMedia import AnkiQuestionMedia
from org_to_anki.ankiConnectWrapper.AnkiConnector import AnkiConnector
from org_to_anki import config

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

    assert('<img src="image.png" style="' in actualDeck.getQuestions()[2].getAnswers()[0])
    assert('width:100px;' in actualDeck.getQuestions()[2].getAnswers()[0])
    assert('height:100px;' in actualDeck.getQuestions()[2].getAnswers()[0])

def testImageWithSize_url():

    filename = "tests/testData/image_url.org"
    actualDeck = parseData.parse(os.path.abspath(filename))

    # Test that comments are removed from the line
    assert("#" not in actualDeck.getQuestions()[0].getAnswers()[0])

def testImagesAreLazyLoad():

    # Set config
    config.lazyLoadImages = True

    try:
        filename = "tests/testData/image_url.org"
        actualDeck = parseData.parse(os.path.abspath(filename))

        assert(actualDeck.getMedia()[0].lazyLoad == True)
        assert(actualDeck.getMedia()[0].data == None)

        # Test image can still be loaded
        actualDeck.getMedia()[0].lazyLoadImage()

        assert(actualDeck.getMedia()[0].lazyLoad == False)
        assert(actualDeck.getMedia()[0].data != None)

    finally:
        # Revert config to default
        config.lazyLoadImages = False


