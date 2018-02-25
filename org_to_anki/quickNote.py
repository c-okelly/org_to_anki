import os

def quickNote():

    # dir = os.path.dirname(__file__)
    # filePath = os.path.join(dir, '../orgNotes/quickNotes.org')
    filePath = "/Users/cokelly/orgNotes/quickNotes.org"
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
