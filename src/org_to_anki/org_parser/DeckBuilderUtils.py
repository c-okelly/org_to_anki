from ..ankiClasses.AnkiDeck import AnkiDeck
from .ParserUtils import getImageFromUrl
from .ParserUtils import convertLineToParameters

import os
import re
import hashlib

class DeckBuilderUtils:

    # Used to check if extra data is containted within the line
    def parseAnswerLine(self, answerLine, filePath, currentDeck): # (str, str, AnkiDeck)

        # Check if line needs to be parsed
        if "[" in answerLine and "]" in answerLine:
            # Image metadata
            potentialLineParamtmeters = {}
            if len(answerLine.split("#")) > 1:
                potentialLineParamtmeters = convertLineToParameters(answerLine.split("#")[1].strip())

            if "http" in answerLine or "www." in answerLine:
                if "[image=" in answerLine:
                    print("Trying to get image using: " + answerLine)

                    # TODO names should make some sense
                    potentialUrls = re.findall("\[image=[^]]+\]", answerLine.strip())
                    if len(potentialUrls) != 0:
                        urlSection = potentialUrls[0]
                        url = urlSection.split("=")[1][:-1]
                        imageData = getImageFromUrl(url)
                        print(hashlib.md5(url.encode()).hexdigest())
                        urlName = "downloaded_image_" + hashlib.md5(url.encode()).hexdigest()
                        currentDeck.addImage(urlName, imageData)

                        imageHtml = self.buildImageLine(urlName, potentialLineParamtmeters)
                        formattedAnswerLine = answerLine.split(urlSection)[0] + imageHtml + answerLine.split(urlSection)[1]

                        return formattedAnswerLine

            # Get image from local file
            elif answerLine.count("[") == 1 and answerLine.count("]") == 1:
                relativeImagePath = answerLine.split("[")[1].split("]")[0]
                fileName = os.path.basename(relativeImagePath)
                baseDirectory = os.path.dirname(filePath) 
                imagePath = os.path.join(baseDirectory, relativeImagePath)

                if len(relativeImagePath) > 0 and os.path.exists(imagePath) and os.path.isfile(imagePath):
                    with open(imagePath, "rb") as file:
                        data = file.read()
                        currentDeck.addImage(fileName, data)

                    answerLine = self.buildImageLine(os.path.basename(imagePath), potentialLineParamtmeters)

                    return answerLine

                else:
                    print("Could not find image on line:", answerLine)
            else:
                print("Could not parse image from line: " + answerLine)
        
        return answerLine
    
    def buildImageLine(self, imagePath, paramters={}):

        # Check if any specific line paramters
        if len(paramters) > 0:
            styles = ""
            for key in paramters.keys():
                styles += "{}:{};".format(key, paramters.get(key))
            return '<img src="{}" style="{}" />'.format(imagePath, styles)
        else:
            return '<img src="{}" />'.format(imagePath)

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
