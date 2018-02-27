import os
from . import config


def createQuickNotesFile():

    directory = config.quickNotesDirectory
    if not os.path.exists(directory):
        os.makedirs(directory)


def getQuickNotesFileName():

    return "quickNotes.org"

if __name__ == "__main__":
    print(getQuickNotesFileName())
