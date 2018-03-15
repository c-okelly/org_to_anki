from .AnkiQuestion import AnkiQuestion


class AnkiDeck:

    # TODO flesh out to represent whole file of multiple types
    # Basic file => represented in a single deck
    # MultiDeck file => File will have mutiple subdecks of general topic
    # represented by file
    def __init__(self, name: str, parentDecks: [str] =None):
        self.deckName = name
        self._parentDecks = parentDecks
        self.ankiQuestions = []

        self.subDecks = []
        self._hasSubDecks = False

    def getQuestions(self):
        return self.ankiQuestions

    def getDeckNames(self):
        names = [self.deckName]
        if self._hasSubDecks:
            for i in self.subDecks:
                names.extend(i.getDeckNames())

        return names

    def addQuestion(self, ankiQuestion: AnkiQuestion):
        self.ankiQuestions.append(ankiQuestion)

    def addSubdeck(self, ankiDeck):
        self.subDecks.append(ankiDeck)
        self._hasSubDecks = True

    def hasSubDeck(self):
        return self._hasSubDecks

    def __eq__(self, other):
        return self.deckName == other.deckName and self._parentDecks == self._parentDecks and self.ankiQuestions == other.ankiQuestions and self.subDecks == other.subDecks
