
class AnkiQuestion:

    def __init__(self, question: str):
        self.deckName = None
        self.question = question
        self._answers = []
        self._tags = []
        self._comments = []
        self._parameters = {}

    def setDeckName(self, deckName: str):
        self.deckName = deckName

    def getDeckName(self):
        return self.deckName

    def updateQuestion(self, question: str):
        self.question = question

    # Getters and setters #
    def addAnswer(self, answer: str):
        self._answers.append(answer)

    def getAnswers(self):
        return self._answers

    def addComment(self, comment: str):
        self._comments.append(comment)

    def getComments(self):
        return self._comments

    def addParameter(self, key: str, value: str):
        self._parameters[key] = value

    def getParameter(self, key):
        return self._parameters.get(key, None)

    def addTag(self, tag: str):
        self._tags.append(tag)

    def getTags(self):
        return self._tags

    # String representation
    def __str__(self):
        return ("DeckName: %s. Question: %s. \nAsnwers: %s. \nTags: %s.\nComments: %s.\nParameters: %s,\nMedia: %s") % (
            self.deckName, self.question, self.getAnswers(), self.getTags(), self.getComments(), self._parameters, self._media)

    # Comparioson to other questions
    def __eq__(self, other):
        if not isinstance(other, AnkiQuestion):
            return False

        return self.question == other.question and self.getAnswers() == other.getAnswers() and self.getTags() == other.getTags(
        ) and self.deckName == other.deckName and self.getComments() == other.getComments() and self._parameters == other._parameters
