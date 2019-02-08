from bs4 import BeautifulSoup
import re
# This should parse either libre office / microsoft office 
# files with bullet points into the expected format

def convertBulletPointsDocument(filePath):

    # Will determine if word or libreOffice document

    if checkDocumentType(filePath) == "word":
        return _parseWordBulletPoints(filePath)
    elif checkDocumentType(filePath) == "libreOffice":
        return _parseLibreOfficeBulletPoints(filePath)

def checkDocumentType(filePath):

    htmlFile = open(filePath, encoding="latin-1")
    soup = BeautifulSoup(htmlFile, 'html.parser')

    numberLists = len(soup.find_all("ul"))

    # Check if there are any html list => these are not present in word files
    if numberLists == 0:
        return "word"
    else: 
        return "libreOffice"

def _parseWordBulletPoints(filePath):

    htmlFile = open(filePath, encoding="latin-1")
    soup = BeautifulSoup(htmlFile, 'html.parser')

    # Word file
    parsedFile = ""
    paragraphs = soup.find_all('p')

    for line in paragraphs:

        if (len(line.text.strip()) == 0):
            continue

        text = line.text.split("\n")
        style = ""
        if (line.has_attr("style")):
            style = line["style"]

        # TODO bullet points or # seem to be split by a line break in raw foramt. 
        # need to redesign how text is parsed here
        if (text[0] == "#"):
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

    return parsedFile.strip()

def _parseLibreOfficeBulletPoints(filePath):


    htmlFile = open(filePath, encoding="latin-1")
    soup = BeautifulSoup(htmlFile, 'lxml')

    parsedFile = ""
    
    # x = soup.body.contents
    # print(x)
    # print()

    bodyContents = soup.body.contents

    for section in bodyContents:

        # print()
        # print(section.name)

        if section.name == "p":
            if len(section.text.strip()) != 0:
                parsedFile += section.text + "\n"

        elif section.name == "ul":
            # print("list")
            # print(section)
            formattedList = _processHtmlList(section)
            parsedFile += formattedList + "\n"
            # break

        elif section.name == None:
            continue
            # print("unknown type")

    return parsedFile.strip()

def _processHtmlList(soupHtmlList, level=1):

    formatedList = ""

    # print(soupHtmlList.contents)
    # print()
    # print("scanner")

    for i in soupHtmlList.contents:
        # print("i section")
        # print(i)
        # print()
        if i.name == "li":
            # print("list")
            # print()
            for k in i.contents:
                # print("k is => ", k.name, ". k => ", k)
                if (k.name == "p"):
                    stars = "*" * level
                    newText = _formatText(k.text)
                    # TODO => only supports either comments or bullet points
                    if newText[0] != "#": 
                        newText = stars + " " + newText
                    formatedList += newText + "\n"
                elif (k.name == "ul"):
                    newLevel = level + 1
                    formatedList += _processHtmlList(k, newLevel) + "\n"
                else:
                    continue

    # print(formatedList)
    return formatedList.strip()

def _formatText(text):

    formattedText = ""
    splitText = text.split("\n")

    for i in splitText:
        formattedText += i.strip() + " "
    
    return formattedText.strip()

