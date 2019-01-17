import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import DocxConverter


def testDocxFileIsCorrectlyConvertered():

    expectedData = ['# Baisc document example', '# Quick Anki notes', '* What is the capital of Ireland?', '** Dublin', '* What is the capital of Germany', '** Berlin']

    filename = "tests/testData/basic.docx"
    linesOfData = DocxConverter.convertDocxToOrgFormat(filename)

    print(linesOfData)

    assert(linesOfData == expectedData)

