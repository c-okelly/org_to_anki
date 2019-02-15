# Differnet imports if within Anki app
# try:
# from bs4 import BeautifulSoup
## TODO => realtive import
from bs4 import BeautifulSoup
# except:
# from BeautifulSoup import BeautifulSoup

import re
import codecs
import chardet


## TODO => review these
import io
try: # Anki import 
    from aqt.utils import showInfo
except:
    pass
# This should parse either libre office / microsoft office 
# files with bullet points into the expected format

def convertBulletPointsDocument(filePath):

    # Will determine if word or libreOffice document

    documentType = checkDocumentType(filePath)
    if documentType == "word":
        return _parseWordBulletPoints(filePath)
    elif documentType == "libreOffice":
        return _parseLibreOfficeBulletPoints(filePath)

def checkDocumentType(filePath):

    # TODO wrap in a try catch that give the user some useful information
    htmlFile = codecs.open(filePath, 'r', "utf-8")
    soup = BeautifulSoup(htmlFile, 'html.parser')


    # TODO => change backFindAll for python3
    numberLists = len(soup.findAll("ul"))

    # Check if there are any html list => these are not present in word files
    if numberLists == 0:
        return "word"
    else: 
        return "libreOffice"

# Ahh word files. Good dam it they do some annoying things. If you save a word file 
# as a web pagethe first time it's charset will be utf-8. If you open this file (in word) and save it again
# it will change to some form of utf-16 little or big endian but with no BOM. Don't do this
# I could support this by checking the chartset and then determining the system endian
def _parseWordBulletPoints(filePath):
 
    htmlFile = codecs.open(filePath, 'r', "utf-8")
    soup = BeautifulSoup(htmlFile, 'html.parser')

    # Word file
    parsedFile = ""
    paragraphs = soup.find_all('p')
    # showInfo(str(paragraphs))

    for line in paragraphs:

        if (len(line.text.strip()) == 0):
            continue

        text = line.text.split("\n")
        style = ""
        if (line.has_attr("style")):
            style = line["style"]

        # TODO bullet points or # seem to be split by a line break in raw foramt. 
        # need to redesign how text is parsed here
        print(text)
        if (text[0].strip() == "#"):
            text[1] = "# " + text[1]

        # Get level of indentation
        regexString = "(\\s)level(\\d{1,2})"
        p = re.compile(regexString)

        searchResult = p.search(style)
        level = None
        if searchResult != None:
            foundString = searchResult.group().strip()
            level = int(foundString[5:])
            # print("level is => ",foundString[5:])
        
        # Format text and remove bullet point if exists
        if len(text) > 1:
            text = text[1]
        else:
            text = text[0]
        # Clean up text
        text = text.replace(u'\xa0', u'')

        if level != None:
            newLine = ("*" * level) + " " + text
        else:
            newLine = text

        if len(newLine) != 0:
            parsedFile += newLine + "\n"

    # showInfo("Word")
    # showInfo(str(parsedFile))
    return parsedFile.strip()

def _parseLibreOfficeBulletPoints(filePath):


    # TODO => python2 => io
    htmlFile = open(filePath, encoding="utf-8")
    # htmlFile = io.open(filePath, encoding="utf-16")
    # with open(filePath, 'r') as file:
    #     htmlFile = file.read()
    soup = BeautifulSoup(htmlFile, 'html.parser')

    parsedFile = ""

    bodyContents = soup.body.contents

    for section in bodyContents:

        if section.name == "p":
            if len(section.text.strip()) != 0:
                parsedFile += section.text + "\n"

        elif section.name == "ul":
            formattedList = _processHtmlList(section)
            parsedFile += formattedList + "\n"

        elif section.name == None:
            continue

    # showInfo("Libre office")
    # showInfo(str(type(parsedFile)))
    return parsedFile.strip()

def _processHtmlList(soupHtmlList, level=1):

    formatedList = ""

    for i in soupHtmlList.contents:
        if i.name == "li":
            for k in i.contents:
                if (k.name == "p"):
                    stars = "*" * level
                    newText = _formatText(k.text)
                    if (isinstance(newText, str) == False):
                        newText = newText.encode("utf-8")

                    # TODO => only supports either comments or bullet points
                    if newText[0] != "#": 
                        newText = stars + " " + newText
                    formatedList += newText + "\n"
                elif (k.name == "ul"):
                    newLevel = level + 1
                    formatedList += _processHtmlList(k, newLevel) + "\n"
                else:
                    continue

    return formatedList.strip()

def _formatText(text):

    formattedText = ""
    splitText = text.split("\n")

    for i in splitText:
        formattedText += i.strip() + " "
    
    return formattedText.strip()

