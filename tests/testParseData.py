import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck

def test_basic_parseData():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)

    expectedDeck = AnkiDeck("basic")
    #build Question
    expectedQuestion = AnkiQuestion.AnkiQuestion("Put request", "basic")
    expectedQuestion.addAnswer("Puts file / resource at specific url")
    expectedQuestion.addAnswer("If file ==> exists => replaces // !exist => creates")
    expectedQuestion.addAnswer("Request => idempotent")

    expectedDeck.addQuestion(expectedQuestion)

    assert actualDeck == expectedDeck

def test_basic_with_sublevels_parseData():

    filename = "tests/testData/basicWithSublevels.org"
    actualDeck = parseData.parse(filename)

    expectedDeck = AnkiDeck("basicWithSublevels")
    #build Question
    expectedQuestion = AnkiQuestion.AnkiQuestion("What is the difference between .jar and .war files in java", "basicWithSublevels")
    expectedQuestion.addAnswer(".jar => contains libraries / resources / accessories files")
    expectedQuestion.addAnswer(".war => contain the web application => jsp / html / javascript / other files")
    expectedQuestion.addAnswer("* Need for web apps")
    expectedDeck.addQuestion(expectedQuestion)

    assert actualDeck == expectedDeck


def test_format_file():
    filename = "tests/testData/basic.org"
    data = parseData._formatFile(filename)

    assert(len(data) == 6)


def test_sort_data():

    lines = """#Comment 1
    # Indented comment 2

* line 1
** line 2
badlyformated line
""".split("\n")

    assert(len(lines) == 7)
    comments, content, badFormatting = parseData._sortData(lines)

    assert(len(comments) == 2)
    assert(len(content) == 2)
    assert(len(badFormatting) == 1)


def test_convert_comments_to_parameters():

    comments = ["#fileType=basic, secondArg=10", "##file=basic"]
    result = parseData._convertCommentsToParameters(comments)
    expected = {'fileType': 'basic', 'secondArg': '10', 'file': 'basic'} 
    assert(result == expected)

