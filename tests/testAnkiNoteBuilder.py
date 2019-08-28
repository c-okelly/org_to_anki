import sys
sys.path.append('../org_to_anki')

from org_to_anki.ankiConnectWrapper.AnkiConnector import AnkiConnector
from org_to_anki.ankiConnectWrapper.AnkiNoteBuilder import AnkiNoteBuilder
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki import config

def testBuildBasicNote():

    #Build basic quesions
    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    expectedDeckName = config.defaultDeck + config.defaultDeckConnector + "Capitals"
    print(noteData)
    assert(noteData["deckName"] == expectedDeckName)
    assert(noteData["modelName"] == "Basic")
    assert(noteData["tags"] == [])
    assert(noteData["fields"]["Front"] == "Capital of dublin")
    assert(noteData["fields"]["Back"] == "<ul style='list-style-position: inside;'><li>Dublin</li></ul>")
    
def testModelTypeWorks():

    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    q.addParameter("noteType","testType")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["modelName"] == "testType")


def testLegacyModelTypeWorks():

    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    q.addParameter("type","testType")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["modelName"] == "testType")


def testQuestionTypeCorrectlyUsed():

    #Build basic quesions
    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin")
    q.addParameter("type", "Basic (and reversed card)")

    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["modelName"] == "Basic (and reversed card)")

### test question answer string is built correctly using parameters ###
def testBuildNoteForSublists():

    answers = ["first answer", ["sublist 1", ["sublist2"], "back to sublist1"], "second answer"]
    a = AnkiNoteBuilder()
    answerString = a.createAnswerString({}, answers)

    expectedString = "<ul style='list-style-position: inside;'><li>first answer</li><ul style='list-style-position: inside;'><li>sublist 1</li><ul style='list-style-position: inside;'><li>sublist2</li></ul><li>back to sublist1</li></ul><li>second answer</li></ul>"
    assert(answerString == expectedString)

### Next two tests ensure that questions that have an internal multiline string are correctly html formatted ###
def testMultiLineQuestionLine():

    q = AnkiQuestion("Capital Cities\nCapital of dublin")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Front"] == "Capital Cities<br>Capital of dublin")

def testManyMultiLineQuestionLines():

    q = AnkiQuestion("Capital Cities\nCapital of dublin")
    q.addQuestion("Second line")
    q.addAnswer("Dublin")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Front"] == "Capital Cities<br>Capital of dublin <br>Second line <br>")


def testQuestionWithoutListTags():

    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin 1")
    q.addAnswer("Dublin 2")
    q.addParameter("list", "false")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Back"] == "Dublin 1<br>Dublin 2<br>")

def testQuestionOrderedList():

    q = AnkiQuestion("Capital of dublin")
    q.addAnswer("Dublin 1")
    q.addAnswer("Dublin 2")
    q.addParameter("list", "ol")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Back"] == "<ol style='list-style-position: inside;'><li>Dublin 1</li><li>Dublin 2</li></ol>")


# TODO => make build outside of list
def testCodeQuestionBuildsWithListSection():

    q = AnkiQuestion("Capital of dublin")
    q.addCode("python3", ["print('Hello')"])
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    print(noteData["fields"]["Back"])

    assert(noteData["fields"]["Back"] == """<ul style='list-style-position: inside;'><li><div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&#39;Hello&#39;</span>)<br></pre></div> </div></li></ul>""")

def testCodeQuestionBuildsWithListStyle():

    q = AnkiQuestion("Capital of dublin")
    q.addParameter("codeStyle", "manni")
    q.addCode("python3", ["print('Hello')"])
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Back"] == """<ul style='list-style-position: inside;'><li><div style="text-align:left"> <div class="highlight" style="background: #f0f3f3"><pre style="line-height: 125%"><span></span><span style="color: #336666">print</span>(<span style="color: #CC3300">&#39;Hello&#39;</span>)<br></pre></div> </div></li></ul>""")


def testBuildingMultiFieldNotes():

    q = AnkiQuestion("Question")
    q.addAnswer("Answer")
    q.addLineToNamedField("field1", "Value 1")
    q.addLineToNamedField("field1", "Value 2")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    expectedString = "<ul style='list-style-position: inside;'><li>Value 1</li><li>Value 2</li></ul>"
    assert(noteData.get("fields").get("field1", None) != None)
    assert(noteData.get("fields").get("field1") == expectedString)

def testBuildingClozeNotes():

    q = AnkiQuestion("When was Dublin founded {{c1::1204}}")
    q.addAnswer("Some Extra info")
    q.addParameter("type", "Cloze")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Text"] == "When was Dublin founded {{c1::1204}}")
    assert(noteData["fields"]["Extra"] == "<ul style='list-style-position: inside;'><li>Some Extra info</li></ul>")

def testBuildingSingleFieldClozeNote():

    q = AnkiQuestion("When was Dublin founded {{c1::1204}}")
    q.addParameter("type", "Cloze")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])

    assert(noteData["fields"]["Text"] == "When was Dublin founded {{c1::1204}}")
    assert(noteData["fields"]["Extra"] == "")

def testBuildNoteWithTags():

    # Build Generic question
    q = AnkiQuestion("When was Dublin founded {{c1::1204}}")
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    q.addParameter("tags", "a,b,c")

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])
    assert(noteData.get("tags") == ['a', 'b', 'c'])

def testMultiLevelListWith_listEqualToFalseParameter():

    q = AnkiQuestion("Question")
    q.addParameter("list","false")
    q.addAnswer("answer 1")
    q.addAnswer(["sub answer 1"])
    deck = AnkiDeck("Capitals")
    deck.addQuestion(q)

    a = AnkiNoteBuilder()
    noteData = a.buildNote(deck.getQuestions()[0])
    assert(noteData.get("fields").get("Back") == "answer 1<br>sub answer 1<br>")