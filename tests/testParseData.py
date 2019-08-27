import sys
sys.path.append('../src/org_to_anki')

from org_to_anki.org_parser import parseData 
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki.org_parser.DeckBuilder import DeckBuilder


### Test basic deck is parsed and built correctly ###

def testBasicPraseNamedCorrectly():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.deckName == "basic")

def testFileWithNoQuestions():

    filename = "tests/testData/empty.org"
    actualDeck = parseData.parse(filename)

    assert(len(actualDeck.getQuestions()) == 0)

def testBaiscPraseQuestsion():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)
    assert(actualDeck.getQuestions()[0].question[0] == "Put request")
    assert(actualDeck.getQuestions()[0].getAnswers() == ["Puts file / resource at specific url", "If file ==> exists => replaces // !exist => creates", "Request => idempotent"])

def testBasicParseMainDeckParameters():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck._comments == ['# Quick Anki notes', '# listType = bulletPoints'])
    assert(actualDeck._parameters == {'listType': 'bulletPoints'})

def testBasicParseQuestionsHaveParametersAndParameters():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)

    params = {'other': 'test', 'listType': 'bulletPoints'} # List type if inherited from parent deck
    comments = ['# other=test']
    assert(actualDeck.getQuestions()[0]._parameters == params)
    assert(actualDeck.getQuestions()[0]._comments == comments)

### Test basic deck parse with sublevels ###

def testBasicWithSublevelsAnswers():

    filename = "tests/testData/basicWithSublevels.org"
    actualDeck = parseData.parse(filename)

    answers = ['.jar => contains libraries / resources / accessories files', '.war => contain the web application => jsp / html / javascript / other files', ['Need for web apps', ["fourth 1", "fourth 2"], "back to third"]]
    assert(actualDeck.getQuestions()[0]._answers == answers)


def testFormatFile():
    filename = "tests/testData/basic.org"
    data = parseData._formatFile(filename)

    assert(len(data) == 8)


def testSortData():

    lines = """#Comment 1
    # Indented comment 2

* line 1
# type=basic
** line 2
badlyformated line
""".split("\n")

    assert(len(lines) == 8)
    comments, content = DeckBuilder()._sortData(lines)

    assert(len(comments) == 2)
    assert(len(content) == 4)



### Test topics deck built correctly ###

def testTopicsDeckNamedCorrectly():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.deckName == "topicsLayout")

def testTopicsSubDecksNamedCorrectly():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.subDecks[0].deckName == "Capital cites")
    assert(actualDeck.subDecks[1].deckName == "Languages of countries")

def testMainDeckHasComment():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    comments = ['# More advanced org file layout. Each topics has its own questions.', '#fileType = topics']
    assert(actualDeck._comments == comments)

def testMainDeckHasParameters():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    params = {'fileType': 'topics'}
    assert(actualDeck._parameters == params)

def testSubDeck1QuestionHasParamters():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)
    
    params = {'type': 'Basic (and reversed card)'}
    comments = ["# type = basic","#type=Basic (and reversed card)"]
    assert(actualDeck.subDecks[1].getQuestions()[0]._parameters == params)
    assert(actualDeck.subDecks[1].getQuestions()[0]._comments == comments)

def testSubDeck0HasBasicQuestion():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    q1 = AnkiQuestion("What is the capital of Ireland")
    q1.addAnswer("Dublin")
    q1.deckName = "Capital cites"

    assert(actualDeck.subDecks[0].getQuestions()[0].question[0] == "What is the capital of Ireland")
    assert(actualDeck.subDecks[0].getQuestions()[0]._answers == ["Dublin"])

def testSubDeck1HasBasicQuestion():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.subDecks[1].getQuestions()[0].question[0] == "What are the main languages in Ireland")
    assert(actualDeck.subDecks[1].getQuestions()[0]._answers == ["English", "Irish"])

def testEmptyLinesHandledCorrectly():

    data = ["* Question line 1","","** Answer"]
    
    deckBuilder = DeckBuilder()
    deck = deckBuilder.buildDeck(data, "test Deck", "")

def testMultiLineQuestion():

    data = ["* Question line 1","* Question line 2","** Answer"]
    deckBuilder = DeckBuilder()
    deck = deckBuilder.buildDeck(data, "test Deck", "")

    expectedQuestion = AnkiQuestion()
    q1 = AnkiQuestion("What is the capital of Ireland")
    expectedQuestion.addQuestion("Question line 1")
    expectedQuestion.addQuestion("Question line 2")
    expectedQuestion.addAnswer("Answer")

    assert(deck.getQuestions()[0].question == expectedQuestion.question)
    print(deck.getQuestions()[0]._answers)
    assert(deck.getQuestions()[0]._answers == expectedQuestion._answers)

# Test flat topics layout

def testFlatTopics():

    filename = "tests/testData/flatTopics.org"
    actualDeck = parseData.parse(filename)
    
    question1 = actualDeck.getQuestions()[0]
    assert(question1.getQuestions()[0] == "Capital cites\nWhat is the capital of Ireland")
    assert(question1.getAnswers()[0] == "Dublin")

    question2 = actualDeck.getQuestions()[1]
    assert(question2.getQuestions()[0] == "Capital cites\nWhat is the capital of Germany")
    assert(question2.getAnswers()[0] == "Berlin")

    question3 = actualDeck.getQuestions()[2]
    assert(question3.getQuestions()[0] == "Languages of countries\nWhat is the main languages in Ireland")
    assert(question3.getAnswers()[0] == "Irish")

    question4 = actualDeck.getQuestions()[3]
    assert(question4.getQuestions()[0] == "Languages of countries\nWhat is the main languages in Germany")
    assert(question4.getAnswers()[0] == "German")

def testOrganisedTopics():

    filename = "tests/testData/organisedFile.org"
    actualDeck = parseData.parse(filename)

    question1 = actualDeck.getQuestions()[0]
    assert(question1.getQuestions()[0] == "First main rule of scalability?")
    assert(question1.getAnswers()[0] == "Each server behind load balancer")

    question2 = actualDeck.getQuestions()[1]
    assert(question2.getQuestions()[0] == "What is the main purpose of the factory pattern?")
    assert(question2.getAnswers()[0] == "Allow reference to objects via an interface")

def testOrganisedFlatTopics():

    filename = "tests/testData/organisedFlatFile.org"
    actualDeck = parseData.parse(filename)

    question1 = actualDeck.getQuestions()[0]
    assert(question1.getQuestions()[0] == "Systems design primer\nFirst main rule of scalability?")
    assert(question1.getAnswers()[0] == "Each server behind load balancer")
    assert(question1.getAnswers()[1] == "Contains same codebase and does not store any user related data")

    question2 = actualDeck.getQuestions()[1]
    assert(question2.getQuestions()[0] == "Systems design primer\nWhere should sessions be stored?")
    assert(question2.getAnswers()[0] == "Centralized data store accessible to servers")

    question3 = actualDeck.getQuestions()[2]
    assert(question3.getQuestions()[0] == "Programming design patterns (online version)\nWhat is the main purpose of the factory pattern? (2)")
    assert(question3.getAnswers()[0] == "To allow object creation without exposing the creation logic to client")
    assert(question3.getAnswers()[1] == "Allow reference to objects via an interface")

def testParseCodeInBackQuotes():

    filename = "tests/testData/codeQuestion.org"
    actualDeck = parseData.parse(filename)

    questions = actualDeck.getQuestions()

    assert(questions[0].getCodeLanguage() == "python")
    assert(questions[0].getCodeSection() == ["print(\"hello world\")"])
    assert(questions[1].getCodeLanguage() == "python")
    assert(questions[1].getCodeSection() == ["if (this):", "    print(\"worked\")"])

def testParseCodeIsFormatted():

    filename = "tests/testData/codeQuestion.org"
    actualDeck = parseData.parse(filename)

    questions = actualDeck.getQuestions()

    print(questions[0].getAnswers()[1])
    assert(questions[0].getAnswers()[1] == """<div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #008800; font-weight: bold">print</span>(<span style="background-color: #fff0f0">&quot;hello world&quot;</span>)<br></pre></div> </div>""")
    assert(questions[1].getAnswers()[0] == """<div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #008800; font-weight: bold">if</span> (this):<br>    <span style="color: #008800; font-weight: bold">print</span>(<span style="background-color: #fff0f0">&quot;worked&quot;</span>)<br></pre></div> </div>""")


def testEmptyLinesAreIgnored():

    data = ["* ","** ","* order list","** Answer"]

    deck = parseData._buildDeck(data, "test.org")

    assert(len(deck.getQuestions()) == 1)
    assert(deck.getQuestions()[0].getQuestions() == ["order list"])
    assert(deck.getQuestions()[0].getAnswers() == ["Answer"])

def testStrangeOrgData():

    data = ["* Planner [0/0]", "** Planner [/]", "#type=notes","** Something",":LOGBOOK:","CLOCK: [2019-04-19 Fri 14:27]--[2019-04-19 Fri 14:27] =>  0:00", ":END:","* order list","** Answer"]

    deck = parseData._buildDeck(data, "test.org")

    assert(len(deck.getQuestions()) == 1)
    assert(deck.getQuestions()[0].getQuestions() == ["order list"])
    assert(deck.getQuestions()[0].getAnswers() == ["Answer"])


def testParsingExtraFieldLinesWithMultipleFields():

    data = ["* Question", "** Answer", "#fieldName=Front hint, x=y", "** front hint","#fieldName=Back hint", "** back hint"]

    deck = parseData._buildDeck(data, "test.org")

    assert(len(deck.getQuestions()) == 1)

    assert(deck.getQuestions()[0].getQuestions() == ["Question"])
    assert(deck.getQuestions()[0].getAnswers() == ["Answer"])

    namedFields = deck.getQuestions()[0].getNamedFields()

    assert(len(namedFields))
    # No guarantee of ordering
    if namedFields[0].getFieldName() == "Front hint":
        a, b = 0, 1
    else:
        a, b = 1, 0

    assert(namedFields[a].getFieldName() == "Front hint")
    assert(namedFields[a].getLines() == ["front hint"])
    assert(namedFields[b].getFieldName() == "Back hint")
    assert(namedFields[b].getLines() == ["back hint"])

def testParsingExtraFieldLinesForMultipleQuestions():

    data = ["* Qusetion 1", "** Answer 1", "#fieldName=Front", "** front hint","* Question 2", "** Answer 2"]

    deck = parseData._buildDeck(data, "test.org")

    assert(len(deck.getQuestions()) == 2)
    assert(len(deck.getQuestions()[1].getNamedFields()) == 0)

def testParsingUnicodeCharacters():

    # data = ['* Hello world in Chinese?', '** 你好']

    # deck = parseData._buildDeck(data, "test.org")
    filename = "tests/testData/unicode.org"
    actualDeck = parseData.parse(filename)

    print(actualDeck.getQuestions()[0])
    question = actualDeck.getQuestions()[0]
    assert(question.getQuestions()[0] == "Hello world in Chinese?")
    assert(question.getAnswers()[0] == "你好")


def testOrgFormattingIsParsedWithoutError():

    data = ['* Planning', '  # type = notes', '** Time planner', '   :LOGBOOK:', '   CLOCK: [2019-04-15 Mon 12:52]--[2019-04-15 Mon 13:17] =>  0:25', '   :END:', '**  Sections', '     1. [X] l1', '     13. [ ] l10?']
    deck = parseData._buildDeck(data, "test.org")

    assert(deck)


def testSectionAreConvertedIntoDecksIndependnatlyForOrganisedFile():

    data = ['# fileType=organisedFile ', '* Planning', '  # type = notes', '** Time planner', '* L1 Intro', '** What are the 3 main motivations for malware?', '*** money', '*** hacktivism', '*** nation state', '** What is an APT?', '*** Advanced persistent threat']
    actualDeck = parseData._buildDeck(data, "test.org")

    assert(len(actualDeck.getQuestions()[0].getQuestions()) == 1)
    assert(actualDeck.getQuestions()[0].getQuestions()[0] == "What are the 3 main motivations for malware?")
    assert(actualDeck.getQuestions()[0]._parameters == {'fileType': 'organisedFile'})

def testTopicsDeckHasEachSectionParsedIndependently():
    
    filename = "tests/testData/topicsLayout1.org"
    actualDeck = parseData.parse(filename)

    params = {'type': 'basic'}
    comments = ["#type=basic"]

    assert(len(actualDeck.subDecks) == 2)

    assert(actualDeck.subDecks[0]._comments == [])
    assert(actualDeck.subDecks[0]._parameters == {})

    assert(actualDeck.subDecks[1].getQuestions()[0]._comments == ['# type = basic', '#type=Basic (and reversed card)'])
    assert(actualDeck.subDecks[1].getQuestions()[0]._parameters == {'type': 'Basic (and reversed card)'})

    assert(actualDeck.subDecks[1].getQuestions()[1]._comments == ['# type = basic'])
    assert(actualDeck.subDecks[1].getQuestions()[1]._parameters == {'type': 'basic'})

def testParsingClozeQuestions():

    filename = "tests/testData/cloze.org"
    actualDeck = parseData.parse(filename)

    assert(len(actualDeck.getQuestions()) == 4)

    assert(actualDeck.getQuestions()[0].getQuestions() == ["When was Dublin founded {{c1::1204}}"])
    assert(actualDeck.getQuestions()[0].getAnswers() == ["Some extra info"])
    assert(actualDeck.getQuestions()[0].getParameter("type") == "Cloze")

    # Check can form Cloze card without answer
    assert(actualDeck.getQuestions()[1].getQuestions() == ["When was Dublin founded {{c1::1204}}"])
    assert(actualDeck.getQuestions()[1].getAnswers() == [])

    # Check that 4th questions is not affect by previous cloze types
    assert(actualDeck.getQuestions()[3].getQuestions() == ["Normal Question"])

def testSectionLevelClozeCardsAreIgnored():


    data = ['# cardType=Cloze', '#type=Cloze','* Question 1', '** Answer 1']
    actualDeck = parseData._buildDeck(data, "test.org")

    assert(actualDeck.getQuestions()[0].getParameter("cardType") == None)
    assert(actualDeck.getQuestions()[0].getParameter("type") == None)

def testDeckWithTagsData():

    data = ['# tags=a,b,c', '* Question 1', '** Answer 1']
    actualDeck = parseData._buildDeck(data, "test.org")

    assert(actualDeck.getQuestions()[0].getTags() == ['a', 'b', 'c'])

def testCardsWithTagsData():

    data = ['* Question 1', '# tags=a,b,c', '** Answer 1']
    actualDeck = parseData._buildDeck(data, "test.org")

    assert(actualDeck.getQuestions()[0].getTags() == ['a', 'b', 'c'])

def testClozeQuestionCreatedCorrectly():

    # TODO
    pass