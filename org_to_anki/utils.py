import os


def createQuickNotesFile():

    directory = getSavePath()
    if not os.path.exists(directory):
        os.makedirs(directory)


def getSavePath():

    # TODO set a global vars
    saveDirectory = "orgNotes"
    saveLocation = "~"

    home = os.path.expanduser(saveLocation)
    savePath = home + "/" + saveDirectory
    return savePath
