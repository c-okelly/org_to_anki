import sys
sys.path.append('../org_to_anki')

from org_to_anki.ankiConnectWrapper.AnkiConnector import AnkiConnector
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki import config

def testBuildBasicNote():


    #Build basic quesions
    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiConnector()
    noteData = a._buildNote(deck.getQuestions()[0])

    expectedDeckName = config.defaultDeck + config.defaultDeckConnector + "Capitals"
    print(noteData)
    assert(noteData["deckName"] == expectedDeckName)
    assert(noteData["modelName"] == "Basic")
    assert(noteData["tags"] == [])
    assert(noteData["fields"]["Front"] == "Capital of dublin")
    assert(noteData["fields"]["Back"] == "<ul style='list-style-position: inside;'><li>Dublin</li></ul>")

def testQuestionTypeCorrectlyUsed():

    #Build basic quesions
    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    q.addParameter("type", "Basic (and reversed card)")

    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiConnector()
    noteData = a._buildNote(deck.getQuestions()[0])

    assert(noteData["modelName"] == "Basic (and reversed card)")

### test question answer string is built correctly using parameters ###
def testBuildNoteForSublists():

    answers = ["first answer", ["sublist 1", ["sublist2"], "back to sublist1"], "second answer"]
    a = AnkiConnector()
    answerString = a._createAnswerString(answers)

    expectedString = "<ul style='list-style-position: inside;'><li>first answer</li><ul style='list-style-position: inside;'><li>sublist 1</li><ul style='list-style-position: inside;'><li>sublist2</li></ul><li>back to sublist1</li></ul><li>second answer</li></ul>"
    assert(answerString == expectedString)

### Next two tests ensure that questions that have an internal multiline string are correctly html formatted ###
def testMultiLineQuestionLine():

    q = AnkiQuestion("Capital Cities\nCapital of dublin")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiConnector()
    noteData = a._buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Front"] == "Capital Cities<br>Capital of dublin")

def testManyMultiLineQuestionLines():

    q = AnkiQuestion("Capital Cities\nCapital of dublin")
    q.addQuestion("Second line")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiConnector()
    noteData = a._buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Front"] == "Capital Cities<br>Capital of dublin <br>Second line <br>")