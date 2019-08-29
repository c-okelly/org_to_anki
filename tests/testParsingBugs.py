import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser.DeckBuilder import DeckBuilder

def testDoubleSquareBracketsLine():

    deckBuilder = DeckBuilder()
    content = ["* Match sequential range of characters?", "** [A-C] or [0-5]"]

    deck = deckBuilder.buildDeck(content, "", "", "basic")

    assert(deck.getQuestions()[0].getAnswers()[0] == '[A-C] or [0-5]')


def testUnicodeWhitespace():

    # Caused index out of bounds error previously
    content = ["\xa0", "* SomeString"]

    deckBuilder = DeckBuilder()
    data = deckBuilder._sortData(content)

    assert(data[1][0] == content[1])
