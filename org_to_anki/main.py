#!/usr/bin/env python3
# Script to parse differnet formated org files and upload them to Anki
import sys

from .org_parser import parseData
from .ankiConnectWrapper import AnkiConnector
from . import config


def parseAndUploadOrgFile(filePath=None):

    if filePath is None:
        filePath = _getUploadFilePath()

    if "~" in filePath:
        filePath = filePath.replace("~", config.homePath)

    print("file is ", filePath)
    _parseAndUpload(filePath)

def _getUploadFilePath():

    firstArg = sys.argv[1:2]
    if len(firstArg) < 1 or firstArg == ['-v']:
        print("File was not given. Will upload default file.")
        filePath = config.quickNotesOrgPath
    else:
        filePath = sys.argv[1]

    return filePath


def _parseAndUpload(filePath):

    deck = parseData.parse(filePath)

    connector = AnkiConnector.AnkiConnector()
    connector.uploadNewDeck(deck)


if __name__ == "__main__":
    parseAndUploadOrgFile("/Users/conorokelly/Desktop/Notes/Org_Files/1.orgNotes/quickNotes.org")
