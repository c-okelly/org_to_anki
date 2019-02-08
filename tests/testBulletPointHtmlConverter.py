import sys
from org_to_anki.converters.BulletPointHtmlConverter import parseWordBulletPoints
from org_to_anki.converters.BulletPointHtmlConverter import parseLibreOfficeBulletPoints

sys.path.append('../org_to_anki')

def testWordOsxDocument():
    
    print("Osx word document test")

    filename = "tests/testData/documents/bulletpoint-doc-word-osx.html"
    parsedFile = parseWordBulletPoints(filename)

    # print(parsedFile)
    lines = parsedFile.split("\n")

    assert(len(lines) == 8)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# type=doc")
    assert(lines[2] == "# docType=word")
    assert(lines[3] == "* What is the capital of Ireland")
    assert(lines[4] == "# type = basic")
    assert(lines[5] == "** Dublin")
    assert(lines[6] == "* What is the Capital of Germany")
    assert(lines[7] == "** Berlin")

def testWordWindowsDocument():
    
    print("Windows word document test")

    filename = "tests/testData/documents/bulletpoint-doc-word-windows.htm"
    parsedFile = parseWordBulletPoints(filename)

    # print(parsedFile)
    lines = parsedFile.split("\n")

    assert(len(lines) == 8)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# type=doc")
    assert(lines[2] == "# docType=word")
    assert(lines[3] == "* What is the capital of Ireland")
    assert(lines[4] == "# type = basic")
    assert(lines[5] == "** Dublin")
    assert(lines[6] == "* What is the Capital of Germany")
    assert(lines[7] == "** Berlin")

def testLibreOsxDocument():
    print("Osx libre document test")

    filename = "tests/testData/documents/bulletpoint-doc-libreOffice-osx.html"
    parsedFile = parseLibreOfficeBulletPoints(filename)

    print(parsedFile)

    lines = parsedFile.split("\n")

    assert(len(lines) == 8)
    assert(lines[0] == "# Test document for org to anki")
    assert(lines[1] == "# type=doc")
    assert(lines[2] == "# docType=libre")
    assert(lines[3] == "* What is the capital of Ireland")
    assert(lines[4] == "# type = basic")
    assert(lines[5] == "** Dublin")
    assert(lines[6] == "* What is the Capital of Germany")
    assert(lines[7] == "** Berlin")