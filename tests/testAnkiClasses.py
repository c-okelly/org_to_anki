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

# def testGetAllDeckQuestions():

#     # Create decks
#     parent = AnkiDeck("parent")
#     child = AnkiDeck("child")
#     subChild = AnkiDeck("subChild")

#     child.addSubdeck(subChild)
#     parent.addSubdeck(child)

#     assert(False)

