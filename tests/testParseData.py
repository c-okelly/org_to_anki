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