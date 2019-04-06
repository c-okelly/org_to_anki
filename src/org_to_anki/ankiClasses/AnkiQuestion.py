from .AnkiQuestionMedia import AnkiQuestionMedia
from ..converters.codeHighlighter import highLightCode

class AnkiQuestion:

    def __init__(self, question = None):
        self.deckName = None
        self.question = []
        if question != None:
            self.question.append(question)
        self._answers = []
        self._tags = []
        self._comments = []
        self._parameters = {}
        self._media = []
        self._hasCode = False
        self._codeLanguage = None
        self._codeSection = []

    def setDeckName(self, deckName): # (str)
        self.deckName = deckName

    def getDeckName(self):
        return self.deckName

    def addQuestion(self, question): # (str
        self.question.append(question)
    
    def getQuestions(self):
        return self.question

    def addImage(self, fileName, filePath): 
        with open(filePath, "rb") as file:
            print(filePath)
            self._media.append(AnkiQuestionMedia("image", fileName, file.read()))

    def hasMedia(self):
        return len(self._media) > 0

    def getMedia(self):
        return self._media

    # Getters and setters #
    def addAnswer(self, answer): # (str)
        self._answers.append(answer)

    def getAnswers(self):
        return self._answers

    def addComment(self, comment): # (str)
        self._comments.append(comment)

    def getComments(self):
        return self._comments

    def addParameter(self, key, value): # (str, str)
        self._parameters[key] = value

    def getParameter(self, key, default=None):
        return self._parameters.get(key, default)
    
    def getAllParamters(self):
        return self._parameters.copy()

    def addTag(self, tag): # (str)
        self._tags.append(tag)

    def getTags(self):
        return self._tags
    
    def addCode(self, codeLanguage, codeSection):
        self._codeLanguage = codeLanguage
        self._codeSection = codeSection
        self._hasCode = True
        # Generate formatted code
        formattedCode = self._formatCodeSection(codeLanguage, codeSection)
        self.addAnswer(formattedCode)

    def getCodeLanguage(self):
        return self._codeLanguage

    def getCodeSection(self):
        return self._codeSection
    
    def _formatCodeSection(self, codeLanguage, codeSection):
        codeString = "\n".join(codeSection).strip()
        # TODO check to see if another style has been specified
        fromattedString = highLightCode(codeString, codeLanguage)
        return fromattedString

    # String representation
    def __str__(self):
        return ("DeckName: %s. Question: %s. \nAsnwers: %s. \nTags: %s.\nComments: %s.\nParameters: %s,\nMedia: %s,\nCodeLanguage: %s,\nCode: %s") % (
            self.deckName, self.question, self.getAnswers(), self.getTags(), self.getComments(), self._parameters, self._media, self._codeLanguage, self._codeSection)

    # Comparison to other questions
    def __eq__(self, other):
        if not isinstance(other, AnkiQuestion):
            return False

        return self.question == other.question and self.getAnswers() == other.getAnswers() and self.getTags() == other.getTags(
        ) and self.deckName == other.deckName and self.getComments() == other.getComments() and self._parameters == other._parameters and self.getMedia(
        ) == other.getMedia() and self.getCodeLanguage() == other.getCodeLanguage() and self.getCodeSection() == other.getCodeSection()