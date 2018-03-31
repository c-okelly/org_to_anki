import sys
sys.path.append('../org_to_anki')

from org_to_anki.ankiConnectWrapper.AnkiConnectorUtils import AnkiConnectorUtils

def testBuildPayloadForCreateDeck():

    a = AnkiConnectorUtils
    payload = eval(a._buildPayload('createDeck', {'deck': 'testName'}))
    expectedPayload = {"action": "createDeck", "params": {"deck": "testName"}, "version": 5}
    assert(payload == expectedPayload)