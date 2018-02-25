import os
from os.path import expanduser

def createQuickNotesFile():

    home = expanduser("~")
    directory = home + "/orgNotes"
    if not os.path.exists(directory):
        os.makedirs(directory)
