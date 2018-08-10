import sys, os, base64
sys.path.append('../org_to_anki')

import responses
import requests

from org_to_anki.main import parseAndUploadOrgFile


def testE2EForOrg():
    generalEndToEndForBasic("basic.org")


def testE2EForTxt():
    generalEndToEndForBasic("basic.txt")


@responses.activate
def generalEndToEndForBasic(fileName):
    #https://github.com/getsentry/responses
    responses.add(responses.POST, 'http://127.0.0.1:8765/', status=200)
    #Return response so deck need to be created
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': ['Default', '0. Org Notes'], 'error': None}, status=200)
    #Return creation of deck id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676641, 'error': None}, status=200)
    # Return creation of card id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': [1521151676641], 'error': None}, status=200)

    filePath = os.path.abspath("tests/testData/" + fileName)
    parseAndUploadOrgFile(filePath)

    actualRequest = eval(responses.calls[3].request.body)

    # Deck created
    assert(eval(responses.calls[2].request.body)["action"] == "createDeck") 
    assert(eval(responses.calls[2].request.body)["params"]["deck"] == "0. Org Notes::basic") 

    assert(actualRequest["params"]["notes"][0]["deckName"] == "0. Org Notes::basic")
    assert(actualRequest["params"]["notes"][0]["modelName"] == "Basic")
    assert(actualRequest["params"]["notes"][0]["tags"] == [])
    print(actualRequest["params"]["notes"][0]["fields"]["Front"])
    assert(actualRequest["params"]["notes"][0]["fields"]["Front"] == "Put request")


@responses.activate
def testEndToEndForTopicsWithParams():
    responses.add(responses.POST, 'http://127.0.0.1:8765/', status=200)
    #Return response so deck need to be created
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': ['Default', '0. Org Notes'], 'error': None}, status=200)
    #Return creation main deck and two subdecks 
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676640, 'error': None}, status=200)
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676641, 'error': None}, status=200)
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676642, 'error': None}, status=200)

    # Return creation of card id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': [1522932422323, 1522932422436, 1522932422545, 1522932422665], 'error': None}, status=200)


    filePath = os.path.abspath("tests/testData/topicsLayout.org")
    parseAndUploadOrgFile(filePath)

    # Should create two decks
    assert(eval(responses.calls[2].request.body)["action"] == "createDeck") 
    assert(eval(responses.calls[2].request.body)["params"]["deck"] == "0. Org Notes::topicsLayout") 

    assert(eval(responses.calls[3].request.body)["action"] == "createDeck") 
    assert(eval(responses.calls[3].request.body)["params"]["deck"] == "0. Org Notes::topicsLayout::Capital cites") 

    assert(eval(responses.calls[4].request.body)["action"] == "createDeck") 
    assert(eval(responses.calls[4].request.body)["params"]["deck"] == "0. Org Notes::topicsLayout::Languages of countries") 

    # Should create two notes. The second should be reversed
    actualRequest = eval(responses.calls[5].request.body)

    assert(actualRequest["action"] == "addNotes")

    assert(actualRequest["params"]["notes"][0]["deckName"] == "0. Org Notes::topicsLayout::Capital cites")
    assert(actualRequest["params"]["notes"][0]["modelName"] == "Basic")
    assert(actualRequest["params"]["notes"][0]["fields"]["Front"] == "What is the capital of Ireland")

    assert(actualRequest["params"]["notes"][1]["deckName"] == "0. Org Notes::topicsLayout::Languages of countries")
    assert(actualRequest["params"]["notes"][1]["modelName"] == "Basic (and reversed card)")
    assert(actualRequest["params"]["notes"][1]["fields"]["Front"] == "What are the main languages in Ireland")


@responses.activate
def testImageUploadE2E():
    responses.add(responses.POST, 'http://127.0.0.1:8765/', status=200)
    #Return response so deck need to be created
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': ['Default', '0. Org Notes'], 'error': None}, status=200)
    #Return creation of deck id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676641, 'error': None}, status=200)
    # Return creation of card id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': [1521151676641], 'error': None}, status=200)

    imagePath = os.path.abspath("tests/testData/imageFolder/image.png")
    with open(imagePath, 'rb') as data:
        encodedImage = base64.b64encode(data.read()).decode("utf-8")

    filePath = os.path.abspath("tests/testData/image.org")
    parseAndUploadOrgFile(filePath)
    

    actualRequest = eval(responses.calls[4].request.body)

    assert(actualRequest["params"]["filename"] == "image.png")
    assert(actualRequest["params"]["data"] == encodedImage)