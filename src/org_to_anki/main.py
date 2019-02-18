#!/usr/bin/env python3
# Script to parse differnet formated org files and upload them to Anki
import sys

from .org_parser import parseData
from .ankiConnectWrapper.AnkiConnector import AnkiConnector
from .ankiConnectWrapper import AnkiPluginConnector
from . import config


def parseAndUploadOrgFile(filePath=None, embedded=False):

    # debugMode = False
    # for arg in sys.argv:
    #     if arg == "-d":
    #         debugMode = True
    #         sys.argv.remove(arg)


    if (filePath == None and embedded == True):
        raise Exception("No file path was given while running in embedded mode.")
    elif filePath is None:
        filePath = _getUploadFilePath()

    if "~" in filePath:
        filePath = filePath.replace("~", config.homePath)

    print("file is ", filePath)
    _parseAndUpload(filePath, embedded)

def _getUploadFilePath():

    firstArg = sys.argv[1:2]
    if len(firstArg) < 1 or firstArg == ['-v']:
        print("File was not given. Will upload default file.")
        filePath = config.quickNotesOrgPath
    else:
        filePath = sys.argv[1]

    return filePath


def _parseAndUpload(filePath, embedded=False):

    deck = parseData.parse(filePath)

    if (embedded == False):
        connector = AnkiConnector()
    else:
        connector = AnkiPluginConnector.AnkiPluginConnector()
    connector.uploadNewDeck(deck)


if __name__ == "__main__":
    print("test")
    # parseAndUploadOrgFile("testFile")
