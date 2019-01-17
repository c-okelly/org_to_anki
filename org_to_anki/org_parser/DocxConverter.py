# Convert formetted docx file into org files
from docx import Document

def convertDocxToOrgFormat(filePath):

    linesOfText = []

    document = Document(filePath)

    for line in document.paragraphs:
        if (len(line.text) > 0):
            linesOfText.append(line.text)

    return linesOfText