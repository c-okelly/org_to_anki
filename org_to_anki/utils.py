import os
from . import config


def createQuickNotesFile(directory=None):
    if directory is None:
        directory = config.quickNotesDirectory

    if not os.path.exists(directory):
        os.makedirs(directory)
