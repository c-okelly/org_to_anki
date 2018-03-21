from .AnkiQuestion import AnkiQuestion


class AnkiDeck:

    # Basic file => represented in a single deck
    # MultiDeck file => File will have mutiple subdecks of general topic represented by file
    def __init__(self, name: str):
        self.deckName:str = name
        self._ankiQuestions:[AnkiQuestion] = []
        self.subDecks = []
        self._hasSubDecks = False

    def getQuestions(self, parentName:str = None, joiner: str = '::'):
        ankiQuestions = []

        for question in self._ankiQuestions:
            if parentName != None:
                question.setDeckName(parentName + joiner + self.deckName)
                ankiQuestions.append(question)
            else:
                question.setDeckName(self.deckName)
                ankiQuestions.append(question)
        
        if self._hasSubDecks:
            name = self.deckName
            if parentName != None:
                name = parentName + joiner + self.deckName
            for i in self.subDecks:
                ankiQuestions.extend(i.getQuestions(name))

        return ankiQuestions 

    def getDeckNames(self, parentName:str = None, joiner: str = '::'):
        deckNames = []
        if parentName != None:
            deckNames.append(parentName + joiner + self.deckName)
        else:
            deckNames.append(self.deckName)

        if self._hasSubDecks:
            name = self.deckName
            if parentName != None:
                name = parentName + joiner + self.deckName
            for i in self.subDecks:
                deckNames.extend(i.getDeckNames(name))

        return deckNames

    def addQuestion(self, ankiQuestion: AnkiQuestion):
        self._ankiQuestions.append(ankiQuestion)

    def addSubdeck(self, ankiDeck):
        self.subDecks.append(ankiDeck)
        self._hasSubDecks = True

    def hasSubDeck(self):
        return self._hasSubDecks

    def __eq__(self, other):
        return self.deckName == other.deckName and self.getDeckNames() == other.getDeckNames() and self.getQuestions() == other.getQuestions() and self.subDecks == other.subDecks
