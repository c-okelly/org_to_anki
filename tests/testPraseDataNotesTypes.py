import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData


def testNotesTypeSection():
    ## Note section should be ignored as they define notes that are not anki questions

    filename = "tests/testData/noteTypes.org"
    actualDeck = parseData.parse(filename)

    # assert(actualDeck.getQuestions()[0].getParameter("type") == "notes")
    assert(len(actualDeck.getQuestions()) == 0)