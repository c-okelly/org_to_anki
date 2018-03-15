import sys
sys.path.append('../org_to_anki')

import responses
import requests

from org_to_anki.main import parseAndUploadOrgFile

@responses.activate
def testEndToEnd():
    #https://github.com/getsentry/responses
    responses.add(responses.POST, 'http://127.0.0.1:8765/', status=200)

    parseAndUploadOrgFile()
    assert(1==2)