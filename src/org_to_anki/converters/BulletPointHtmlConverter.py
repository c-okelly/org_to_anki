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

    # Post processing
    parsedFile = _removeSpecialCharacters(parsedFile)

    return parsedFile.strip()

def _parseLibreOfficeBulletPoints(filePath):


    htmlFile = open(filePath, encoding="utf-8")
    soup = BeautifulSoup(htmlFile, 'html.parser')

    parsedFile = ""

    bodyContents = soup.body.contents

    for section in bodyContents:

        if section.name == "p":
            if len(section.text.strip()) != 0:
                parsedFile += section.text + "\n"

        elif section.name == "ul":
            formattedList = _formatBadlyParsedLibreOfficeList(section)
            parsedFile += formattedList + "\n"

        elif section.name == None:
            continue

    # Post processing
    parsedFile = _removeSpecialCharacters(parsedFile)
    parsedFile = _postLibreOfficeTextForCode(parsedFile) 

    return parsedFile.strip()

# LibreOffice does not close the <li> tags used in the html it generates. This causes 
# a parseing issue when building the html tree with the default beautifulsoup parser.
# Ths function is written specifically to correct a for this issue. It should NOT be 
# used to parse correctly formatted html lists
def _formatBadlyParsedLibreOfficeList(soupHtmlList, level=1):

    formatedList = ""

    if len(soupHtmlList.contents[0]) == 0:
        currentListItem = soupHtmlList.contents[1:]
    else:
        currentListItem = soupHtmlList

    for item in currentListItem.contents:

        if (item.name == None):
            continue
        elif (item.name == "p"):
            stars = "*" * level
            formattedLine = _removeLineBreak(item.text)

            if len(formattedLine.strip()) == 0: # Empty line
               pass 
            elif formattedLine[0] != "#": 
                formattedLine = stars + " " + formattedLine

            formatedList += formattedLine + "\n"
        elif (item.name == "ul"):
            newLevel = level + 1
            formatedList += _formatBadlyParsedLibreOfficeList(item, newLevel)
        elif (item.name == "li"):
            formatedList += _formatBadlyParsedLibreOfficeList(item, level)
        else:
            print("error")
        
    return formatedList

def _removeLineBreak(text):

    if "\n" not in text:
        return text

    formattedText = ""
    for i in text.split("\n"):
        formattedText += i.strip() + " "
    return formattedText.strip()


def _removeSpecialCharacters(text):

    # Unicode quote marks
    text = text.replace("“","\"")
    text = text.replace("”","\"")

    return text

def _postLibreOfficeTextForCode(text):

    formattedText = ""
    lines = text.split("\n")

    while len(lines) > 0:
        line = lines.pop(0)
        sections = line.split(" ")
        initialAsteriskCount = 0
        if len(sections) > 1 and sections[1].startswith("```"):
            initialAsteriskCount = len(sections[0])
            formattedText += line[initialAsteriskCount+1:] + "\n"
            while True:
                line = lines.pop(0)
                sections = line.split(" ")
                # Reach end of code section
                if len(sections) > 1 and sections[1].startswith("```"):
                    noAsterisk = len(sections[0])
                    formattedText += line[noAsterisk:].strip() + "\n"
                    break
                # Create standard line
                else:
                    noAsterisk = len(sections[0])
                    indentation = noAsterisk - initialAsteriskCount
                    formattedText += ("\t" * indentation) + line[noAsterisk+1:] + "\n"
        else:
            formattedText += line + "\n"

    return(formattedText)