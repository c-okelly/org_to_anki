import sys
import os
sys.path.append('../org_to_anki')

# Anki deck
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.NamedNoteField import NamedNoteField
from org_to_anki.ankiClasses.AnkiQuestionMedia import AnkiQuestionMedia
from org_to_anki.ankiClasses.AnkiQuestionFactory import AnkiQuestionFactory

def testGettingDeckNames():

    # Create deck with subdeck
    parent = AnkiDeck("parent")
    child = AnkiDeck("child")
    subChild = AnkiDeck("subChild")

    child.addSubdeck(subChild)
    parent.addSubdeck(child)

    deckNames = parent.getDeckNames()

    assert(deckNames == ["parent", "parent::child", "parent::child::subChild"])

def testDeckNameSetFor_GetAllDeckQuestion():

    parent = AnkiDeck("parent")
    child = AnkiDeck("child")
    subChild = AnkiDeck("subChild")

    child.addSubdeck(subChild)
    parent.addSubdeck(child)

    # Expected question
    expectedQuestion1 = AnkiQuestion("What is the capital of Ireland")
    expectedQuestion1.addAnswer("Dublin")
    expectedQuestion1.setDeckName("parent")

    expectedQuestion2 = AnkiQuestion("What is the capital of France")
    expectedQuestion2.addAnswer("Paris")
    expectedQuestion2.setDeckName("parent::child")

    expectedQuestion3 = AnkiQuestion("What is the capital of Germany")
    expectedQuestion3.addAnswer("Berlin")
    expectedQuestion3.setDeckName("parent::child::subChild")

    # Add questions
    firstQuestion = AnkiQuestion("What is the capital of Ireland")
    firstQuestion.addAnswer("Dublin")
    parent.addQuestion(firstQuestion)

    secondQuestion = AnkiQuestion("What is the capital of France")
    secondQuestion.addAnswer("Paris")
    child.addQuestion(secondQuestion)

    thirdQuestion = AnkiQuestion("What is the capital of Germany")
    thirdQuestion.addAnswer("Berlin")
    subChild.addQuestion(thirdQuestion)

    # Comprae
    questions = parent.getQuestions()

    assert(questions == [expectedQuestion1, expectedQuestion2, expectedQuestion3])


def testCommentsAndParametersForAnkiQuestion():

    q = AnkiQuestion("Test question")
    q.addAnswer("Test Answer")
    q.addTag("test tag")
    q.addComment("Test comment")
    q.addParameter("type", "basic")
    q.addParameter("type1", "basic1")

    assert(q.getAnswers() == ["Test Answer"])
    assert(q.getTags() == ["test tag"])
    assert(q.getComments() == ["Test comment"])
    assert(q.getParameter("type") == "basic")
    assert(q.getParameter("type1") == "basic1")
    assert(q.getParameter("notFound") == None)


def testQuestionInheritParamsFromDeck():


    q1 = AnkiQuestion("Test question")
    q1.addAnswer("Test Answer")
    q1.addParameter("type", "reversed")

    deck = AnkiDeck("Test Deck")
    deck.addParameter("type1", "basic1")
    deck.addParameter("type", "basic")
    deck.addQuestion(q1)

    questions = deck.getQuestions()

    assert(questions[0].getParameter("type") == "reversed")
    assert(questions[0].getParameter("type1") == "basic1")

def testDecksInheritParamsFromParentDeck():

    q1 = AnkiQuestion("Test question")
    q1.addAnswer("Test Answer")
    q1.addParameter("q0", "question")

    deck0 = AnkiDeck("deck0")
    deck0.addParameter("deck0", "deck0")
    deck0.addQuestion(q1)

    deck1 = AnkiDeck("deck1")
    deck1.addParameter("deck1", "deck1")
    deck1.addSubdeck(deck0)

    deck2 = AnkiDeck("deck2")
    deck2.addParameter("deck2", "deck2")
    deck2.addParameter("deck1", "deck2")
    deck2.addParameter("deck0", "deck2")
    deck2.addParameter("q0", "deck2")
    deck2.addSubdeck(deck1)

    questions = deck2.getQuestions()

    assert(questions[0].getParameter("deck2") == "deck2")
    assert(questions[0].getParameter("deck1") == "deck1")
    assert(questions[0].getParameter("deck0") == "deck0")
    assert(questions[0].getParameter("q0") == "question")

def testGetMediaMethod():

    # Create deck with subdeck
    parent = AnkiDeck("parent")
    parent._media = ['p']
    child = AnkiDeck("child")
    child._media = ['c']
    subChild = AnkiDeck("subChild")
    subChild._media = ['sc']

    child.addSubdeck(subChild)
    parent.addSubdeck(child)

    assert(parent.getMedia() == ['sc', 'c', 'p'])

def testAddImageForAnkiQuestion():

    fullImagePath = os.path.abspath("tests/testData/imageFolder/image.png")

    deck = AnkiDeck("Test deck")
    question = AnkiQuestion("test question")
    deck.addQuestion(question)
    question.addImage("image.png", fullImagePath)

    with open(fullImagePath, 'rb') as data:
        mediaItem = AnkiQuestionMedia("image", "image.png", data.read())

    assert(mediaItem == question.getMedia()[0])


def testAddMultiLineQuestion():

    deck = AnkiDeck("Test deck")
    questionFactory = AnkiQuestionFactory("test", "")

    questionFactory.addQuestionLine(" test question\n second line")
    questionFactory.addAnswerLine("answer")

    q = questionFactory.buildQuestion()

    assert(q.question[0] == "test question\nsecond line")


def testCreationOfNamedNoteFieldWithinAnkiQuestion():

    a = AnkiQuestion("question")
    a.addAnswer("answer")

    a.addNoteField("testField")
    a.addLineToNamedField("testField", "data")

    namedFields = a.getNamedFields()

    namedFields = a.getNamedFields()
    n = NamedNoteField("testField")
    n.addLine("data")
    assert(namedFields[0] == n)

def testMultipleNamedNoteField():

    a = AnkiQuestion("question")
    a.addAnswer("answer")

    a.addLineToNamedField("testField", "data")
    a.addLineToNamedField("testField1", "data1")
    namedFields = a.getNamedFields()

    # No guarantee of ordering
    if namedFields[0].getFieldName() == "testField":
        a, b = 0, 1
    else:
        a, b = 1, 0

    assert(namedFields[a].getFieldName() == "testField")
    assert(namedFields[a].getLines() == ["data"])
    assert(namedFields[b].getFieldName() == "testField1")
    assert(namedFields[b].getLines() == ["data1"])

def testNameNoteField():

    n = NamedNoteField("name")
    n.addLine("new line")
    assert(n.getFieldName() == "name")
    assert(n.getLines() == ["new line"])

def testAnkiQuestionFactoryAnswerMetaDataSystem():

    a = AnkiQuestionFactory("test", "")

    metadata = {}
    a.addAnswerLine("** a1")

    metadata["fieldName"] = "1"
    metadata["x"] = "y"
    a.addAnswerLine("** a2", metadata)

    metadata["fieldName"] = "2"
    a.addAnswerLine("** a3", metadata)

    data = a.currentAnswers

    # Test metadata remains empty
    assert(data[0].get("line") == "** a1")
    assert(data[0].get("metadata") == {})

    # Test metadata set and not overwritten by latter update
    assert(data[1].get("line") == "** a2")
    assert(data[1].get("metadata") == {'fieldName': '1', 'x': 'y'})

    # Test data is updated
    assert(data[2].get("line") == "** a3")
    assert(data[2].get("metadata") == {'fieldName': '2', 'x': 'y'})

