from ..ankiClasses.AnkiDeck import AnkiDeck

import os

class QuestionBuilderUtils:

    # Used to check if extra data is containted within the line
    def parseAnswerLine(self, answerLine: str, filePath: str, currentDeck: AnkiDeck):

        # Check if line needs to be parsed
        if "[" in answerLine and "]" in answerLine:
            if "http://" in answerLine or "www." in answerLine:
                raise Exception("Line could not be parsed: " + answerLine)

            elif answerLine.count("[") == 1:
                relativeImagePath = answerLine.split("[")[1].split("]")[0]
                fileName = os.path.basename(relativeImagePath)
                baseDirectory = os.path.dirname(filePath) 
                imagePath = os.path.join(baseDirectory, relativeImagePath)

                if len(relativeImagePath) > 0 and os.path.exists(imagePath):

                    currentDeck.addImage(fileName, imagePath)
                    answerLine = '<img src="' + os.path.basename(imagePath) + '" />'
                else:
                    print("Could not find image on line:", answerLine)

            else:
                raise Exception("Line could not be parsed: " + answerLine)
        
        return answerLine

    def removeAstrics(self, line: str):
        line = line.strip().split(" ")[1:]
        line = " ".join(line)
        return line

    def countAstrics(self, line: str):
        return line.split(' ')[0].count('*', 0, 10)

    def generateSublist(self, subItems: [str]):

        formatedList = []

        indentaionLevel = self.countAstrics(subItems[0])
        for item in subItems:
            if self.countAstrics(item) == indentaionLevel:
                formatedList.append(item)
            elif self.countAstrics(item) > indentaionLevel and isinstance(formatedList[-1], list):
                formatedList[-1].append(item)
            else:
                formatedList.append([item])

        cleaned = []
        for i in formatedList:
            if isinstance(i, list):
                cleaned.append(self.generateSublist(i))
            else:
                cleaned.append(self.removeAstrics(i))

        return cleaned
