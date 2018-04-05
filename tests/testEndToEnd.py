import sys
import os
sys.path.append('../org_to_anki')

import responses
import requests

from org_to_anki.main import parseAndUploadOrgFile

@responses.activate
def testEndToEndForBasic():
    #https://github.com/getsentry/responses
    responses.add(responses.POST, 'http://127.0.0.1:8765/', status=200)
    #Return response so deck need to be created
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': ['Default', '0. Org Notes'], 'error': None}, status=200)
    #Return creation of deck id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': 1521151676641, 'error': None}, status=200)
    # Return creation of card id
    responses.add(responses.POST, 'http://127.0.0.1:8765/', json={'result': [1521151676641], 'error': None}, status=200)


    filePath = os.path.abspath("tests/testData/basic.org")
    parseAndUploadOrgFile(filePath)

    actualRequest = eval(responses.calls[3].request.body)

    # Deck created
    assert(eval(responses.calls[2].request.body)["action"] == "createDeck") 
    assert(eval(responses.calls[2].request.body)["params"]["deck"] == "0. Org Notes::basic") 

    assert(actualRequest["params"]["notes"][0]["deckName"] == "0. Org Notes::basic")
    assert(actualRequest["params"]["notes"][0]["modelName"] == "Basic")
    assert(actualRequest["params"]["notes"][0]["tags"] == [])
    assert(actualRequest["params"]["notes"][0]["fields"]["Front"] == "Put request")
    assert(actualRequest["params"]["notes"][0]["fields"]["Back"] == "<ul style='list-style-position: inside;'><li>Puts file / resource at specific url</li><li>If file ==> exists => replaces // !exist => creates</li><li>Request => idempotent</li></ul>")


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