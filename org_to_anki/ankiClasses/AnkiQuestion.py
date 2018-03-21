class AnkiQuestion:

    def __init__(self, question: str):
        self.deckName = None
        self.tags = []
        self.question = question
        self.answers = []

    def setDeckName(self, deckName: str):
        self.deckName = deckName

    def updateQuestion(self, question: str):
        self.question = question

    def addAnswer(self, answer: str):
        self.answers.append(answer)

    def addTag(self, tag: str):
        self.tags.append(tag)

    def __str__(self):
        return ("DeckName: %s. Question: %s. \nAsnwers: %s. \nTags: %s") % (
            self.deckName, self.question, self.answers, self.tags)

    def __eq__(self, other):
        if not isinstance(other, AnkiQuestion):
            return False

        return self.question == other.question and self.answers == other.answers and self.tags == other.tags and self.deckName == other.deckName
