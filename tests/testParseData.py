import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses import AnkiQuestion

def test_basic_parseData():

    filename = "tests/testData/basic.org"
    actualQuestion = parseData.parse(filename)[0]

    expectedQuestion = AnkiQuestion.AnkiQuestion("Put request", "basic")
    expectedQuestion.addAnswer("Puts file / resource at specific url")
    expectedQuestion.addAnswer("If file ==> exists => replaces // !exist => creates")
    expectedQuestion.addAnswer("Request => idempotent")

    assert actualQuestion == expectedQuestion