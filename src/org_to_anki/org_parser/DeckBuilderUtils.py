from ..ankiClasses.AnkiDeck import AnkiDeck

import os

class DeckBuilderUtils:

    # Used to check if extra data is containted within the line
    def parseAnswerLine(self, answerLine, filePath, currentDeck): # (str, str, AnkiDeck)

        # Check if line needs to be parsed
        if "[" in answerLine and "]" in answerLine:
            # print(answerLine)
            # print(filePath)
            if "http://" in answerLine or "www." in answerLine:
                raise Exception("Line could not be parsed: " + answerLine)

            elif answerLine.count("[") == 1:
                relativeImagePath = answerLine.split("[")[1].split("]")[0]
                fileName = os.path.basename(relativeImagePath)
                baseDirectory = os.path.dirname(filePath) 
                imagePath = os.path.join(baseDirectory, relativeImagePath)

                if len(relativeImagePath) > 0 and os.path.exists(imagePath) and os.path.isfile(imagePath):

                    currentDeck.addImage(fileName, imagePath)
                    answerLine = '<img src="' + os.path.basename(imagePath) + '" />'
                else:
                    print("Could not find image on line:", answerLine)
            else:
                print("Could not parse image from line: " + answerLine)
        
        return answerLine

    def removeAsterisk(self, line): # (str)
        if line.strip()[0] == "*":
            line = line.strip().split(" ")[1:]
            line = " ".join(line)
            return line
        else:
            return line

    def countAsterisk(self, line): # (str)
        return line.split(' ')[0].count('*', 0, 10)

    def generateSublist(self, subItems): # ([str])

        formatedList = []

        indentationLevel = self.countAsterisk(subItems[0])
        for item in subItems:
            if self.countAsterisk(item) == indentationLevel:
                formatedList.append(item)
            elif self.countAsterisk(item) > indentationLevel and isinstance(formatedList[-1], list):
                formatedList[-1].append(item)
            else:
                formatedList.append([item])

        cleaned = []
        for i in formatedList:
            if isinstance(i, list):
                cleaned.append(self.generateSublist(i))
            else:
                cleaned.append(self.removeAsterisk(i))

        return cleaned

    def formatLine(self, line): # (str)

        formattedLine = line

        # Strip extra spaces for multiline
        if "\n" in formattedLine:
            cleanLine = ""
            for i in formattedLine.split("\n"):
                cleanLine += i.strip() + "\n"
            formattedLine = cleanLine.strip()

        return formattedLine
