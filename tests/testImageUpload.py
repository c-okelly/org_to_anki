import sys, os
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses.AnkiQuestionMedia import AnkiQuestionMedia

def testImageTagCorrectProccesed():

    filename = "tests/testData/image.org"
    fullFilePath = os.path.abspath(filename)

    actualDeck = parseData.parse(fullFilePath)

    imageFile = "tests/testData/imageFolder/image.png"
    fullImagePath = os.path.abspath(imageFile)

    with open(fullImagePath, 'rb') as data:
        mediaItem = AnkiQuestionMedia("image", "image.png", data.read())

    assert(mediaItem == actualDeck.getQuestions()[0].getMedia()[0])

def testImageCorrectlyUploaded():

    assert False

def testImageCorrectlySepcifiedWhenRequestBuild():

    assert False