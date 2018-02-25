import os
from . import utils


def quickNote():

    filePath = utils.getSavePath() + "/" + utils.getQuickNotesFileName()

    utils.createQuickNotesFile()

    with open(filePath, "a") as orgFile:

        newQuestion = ""
        question = input("Enter the question.\n").strip()
        newQuestion += "* " + question + "\n"

        answer = ""
        while True:
            answer = input(
                "Enter an answer. Enter blank answer to exit.\n").strip()
            if answer == "":
                break
            else:
                newQuestion += "** " + answer + "\n"

        orgFile.write(newQuestion)


if __name__ == "__main__":
    quickNote()
