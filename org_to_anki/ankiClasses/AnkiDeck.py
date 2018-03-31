from .AnkiQuestion import AnkiQuestion


class AnkiDeck:

    # Basic file => represented in a single deck
    # MultiDeck file => File will have mutiple subdecks of general topic represented by file
    def __init__(self, name: str):
        self.deckName = name
        self.subDecks = []
        self._ankiQuestions = []
        self._parameters = {}
        self._comments = []
        
    
    def addComment(self, comment: str):
        self._comments.append(comment)
    
    def getComments(self):
        return self._comments
    
    def addParameter(self, key: str, value: str):
        self._parameters[key] = value
    
    def getParameter(self, key):
        return self._parameters.get(key, None)

    def getQuestions(self, parentName:str = None, parentParamters:dict = None, joiner: str = '::'):
        ankiQuestions = []

        for question in self._ankiQuestions:
            if parentName != None:
                question.setDeckName(parentName + joiner + self.deckName)
            else:
                question.setDeckName(self.deckName)

            if parentParamters != None:
                for key in parentParamters:
                    if self.getParameter(key) == None:
                        self.addParameter(key, parentParamters[key])

            for key in self._parameters:
                if question.getParameter(key) == None:
                    question.addParameter(key, self._parameters[key])
        
            ankiQuestions.append(question)

        if self.hasSubDeck():
            name = self.deckName
            if parentName != None:
                name = parentName + joiner + self.deckName
            if parentParamters != None:
                for key in parentParamters:
                    if self.getParameter(key) == None:
                        self.addParameter(key, parentParamters[key])

            for i in self.subDecks:
                ankiQuestions.extend(i.getQuestions(name, self._parameters))

        return ankiQuestions 

    def getDeckNames(self, parentName:str = None, joiner: str = '::'):
        deckNames = []
        if parentName != None:
            deckNames.append(parentName + joiner + self.deckName)
        else:
            deckNames.append(self.deckName)

        if self.hasSubDeck():
            name = self.deckName
            if parentName != None:
                name = parentName + joiner + self.deckName
            for i in self.subDecks:
                deckNames.extend(i.getDeckNames(name))

        return deckNames

    def addQuestion(self, ankiQuestion: AnkiQuestion):
        self._ankiQuestions.append(ankiQuestion)

    def addSubdeck(self, ankiDeck): # TODO Should have type of AnkiDeck
        self.subDecks.append(ankiDeck)

    def hasSubDeck(self):
        return len(self.subDecks) > 0

    def __str__(self):
        return ("DeckName: %s.\nSubDecks: %s.\nQuestions: %s.\nParamters: %s.\nComments: %s.") % ( 
        self.deckName, self.subDecks, self._ankiQuestions, self._parameters, self._comments)

    def __eq__(self, other):
        return self.deckName == other.deckName and self.getDeckNames() == other.getDeckNames() and self.getQuestions() == other.getQuestions() and self.subDecks == other.subDecks and self._parameters == other._parameters and self._comments == other._comments
