import os
from org_to_anki import utils
from org_to_anki.utils import createQuickNotesFile

def quickNote():

    # TODO set default save file globally
    quickNotesFile = "quickNotes.org"
    filePath = "/"

    utils.createQuickNotesFile()

    with open(filePath, "a") as orgFile:

        newQuestion = ""
        question = input("Enter the question.\n").strip()
        newQuestion += "* " + question + "\n"

        answer = ""
        while True: 
            answer = input("Enter an answer. Enter blank answer to exit.\n").strip()
            if answer == "":
                break
            else:
                newQuestion += "** " + answer + "\n"

        orgFile.write(newQuestion)

if __name__ == "__main__":
    quickNote()
