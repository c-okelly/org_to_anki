import sys
from org_to_anki.converters.BulletPointHtmlConverter import convertBulletPointsDocument
from org_to_anki.converters.BulletPointHtmlConverter import checkDocumentType
from org_to_anki.org_parser.parseData import parse

sys.path.append('../org_to_anki')

def testWordOsxDocument():
    
    print("Osx word document test")

    filename = "tests/testData/documents/bulletpoint-doc-word-osx.html"
    parsedFile = convertBulletPointsDocument(filename)

    lines = parsedFile.split("\n")

    print(len(lines))
    print(lines)
    assert(len(lines) == 7)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# docType=word")
    assert(lines[2] == "* What is the capital of Ireland")
    assert(lines[3] == "# type = Basic")
    assert(lines[4] == "** Dublin")
    assert(lines[5] == "* What is the Capital of Germany")
    assert(lines[6] == "** Berlin")

def testWordWindowsDocument():
    
    print("Windows word document test")

    filename = "tests/testData/documents/bulletpoint-doc-word-windows.htm"
    parsedFile = convertBulletPointsDocument(filename)

    # print(parsedFile)
    lines = parsedFile.split("\n")

    assert(len(lines) == 7)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# docType=word")
    assert(lines[2] == "* What is the capital of Ireland")
    assert(lines[3] == "# type = Basic")
    assert(lines[4] == "** Dublin")
    assert(lines[5] == "* What is the Capital of Germany")
    assert(lines[6] == "** Berlin")

def testLibreOsxDocument():
    print("Osx libre document test")

    filename = "tests/testData/documents/bulletpoint-doc-libreOffice-osx.html"
    parsedFile = convertBulletPointsDocument(filename)
    print(parsedFile)

    lines = parsedFile.split("\n")

    assert(len(lines) == 8)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# docType=libre")
    assert(lines[2] == "* What is the capital of Ireland")
    assert(lines[3] == "# type = Basic")
    assert(lines[4] == "** Dublin")
    assert(lines[6] == "* What is the Capital of Germany")
    assert(lines[7] == "** Berlin")

def testSecondLibreOsxDocument():
    print("Osx libre document test - 2")

    filename = "tests/testData/documents/bulletpoint-dock-libreOffice-osx-sinlge-multi.html"
    parsedFile = convertBulletPointsDocument(filename)

    lines = parsedFile.split("\n")

    assert(lines[0] == "# lines with # are comments and are ignored")
    assert(lines[1] == "* What is the capital of Ireland?")
    assert(lines[2] == "** Dublin")
    assert(lines[3] == "* What is the capital of France?")
    assert(lines[4] == "** Paris")
    assert(lines[5] == "* What is the capital of Germany?")
    assert(lines[6] == "** Berlin")
    assert(lines[7] == "* What is the capital of Australia?")
    assert(lines[8] == "** Canberra")

def testDocumentTypeDeterminedCorrectly():

    libreOfficeFile = "tests/testData/documents/bulletpoint-doc-libreOffice-osx.html"

    assert(checkDocumentType(libreOfficeFile) == "libreOffice")

    wordWindowsFile = "tests/testData/documents/bulletpoint-doc-word-windows.htm"
    wordOsxFile = "tests/testData/documents/bulletpoint-doc-word-osx.html"

    assert(checkDocumentType(wordOsxFile) == "word")
    assert(checkDocumentType(wordWindowsFile) == "word")

### Component parse test ###

def testBulletPointDocsAreHandeledBy_parseData():

    libreOfficeFile = "tests/testData/documents/bulletpoint-doc-libreOffice-osx.html"
    libreDeck = parse(libreOfficeFile)

    assert(libreDeck.getQuestions()[0].getQuestions()[0] == "What is the capital of Ireland")
    assert(libreDeck.getQuestions()[0].getAnswers()[0] == "Dublin")

    wordWindowsFile = "tests/testData/documents/bulletpoint-doc-word-windows.htm"
    windowsWordDeck = parse(wordWindowsFile)

    assert(windowsWordDeck.getQuestions()[0].getQuestions()[0] == "What is the capital of Ireland")
    assert(windowsWordDeck.getQuestions()[0].getAnswers()[0] == "Dublin")

    wordOsxFile = "tests/testData/documents/bulletpoint-doc-word-osx.html"
    osxWordDeck = parse(wordOsxFile)

    assert(osxWordDeck.getQuestions()[0].getQuestions()[0] == "What is the capital of Ireland")
    assert(osxWordDeck.getQuestions()[0].getAnswers()[0] == "Dublin")