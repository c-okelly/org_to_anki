import sys
import os
sys.path.append('../org_to_anki')

import responses
import requests

from org_to_anki.main import parseAndUploadOrgFile

@responses.activate
def testEndToEnd():
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

    expectedRequest = {"action": "addNotes", "params": {"notes": [{"deckName": "0. Org Notes::basic", "modelName": "Basic", "tags": [], "fields": {"Front": "Put request", "Back": "<ul style='list-style-position: inside;'><li>Puts file / resource at specific url</li><li>If file ==> exists => replaces // !exist => creates</li><li>Request => idempotent</li></ul>"}}]}, "version": 5}
    actualRequest = eval(responses.calls[3].request.body)

    assert(expectedRequest == actualRequest)