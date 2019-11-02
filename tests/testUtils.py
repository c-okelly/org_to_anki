import sys
import os
sys.path.append('../org_to_anki')

from org_to_anki.utils import createQuickNotesFile
from org_to_anki.utils import getAnkiPluginConnector
from org_to_anki.ankiConnectWrapper.AnkiPluginConnector import AnkiPluginConnector


def testCreateFile():
    dir = os.path.dirname(__file__)
    newFilePath = dir + "/" + "orgNotes"
    assert(os.path.exists(newFilePath) == False)
    createQuickNotesFile(newFilePath)
    assert(os.path.exists(newFilePath))
    os.rmdir(newFilePath)
    assert(os.path.exists(newFilePath) == False)

def testGetAnkiPluginConnector():

    connector = getAnkiPluginConnector()
    assert(type(connector) == AnkiPluginConnector)
