import sys
import os
sys.path.append('../org_to_anki')

# Anki deck
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion

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

