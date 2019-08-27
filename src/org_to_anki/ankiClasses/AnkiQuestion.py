from .AnkiQuestionMedia import AnkiQuestionMedia
from .NamedNoteField import NamedNoteField
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
        self._namedNoteFields = {}

    def setDeckName(self, deckName): # (str)
        self.deckName = deckName

    def getDeckName(self):
        return self.deckName

    def addQuestion(self, question): # (str
        self.question.append(question)
    
    def getQuestions(self):
        return self.question

    def addImage(self, fileName, fileData): 
        self._media.append(AnkiQuestionMedia("image", fileName, fileData))

    def hasMedia(self):
        return len(self._media) > 0

    def getMedia(self):
        return self._media

    # Getters and setters #
    def addAnswer(self, answer, fieldName=None): # (str)
        # Check if answer line is for specific field or add to default
        if fieldName is not None:
            self.addLineToNamedField(fieldName, answer)
        else:
            self._answers.append(answer)

    def getAnswers(self):
        return self._answers

    def addComment(self, comment): # (str)
        self._comments.append(comment)

    def getComments(self):
        return self._comments

    def addParameter(self, key, value): # (str, str)
        self._parameters[key] = value

        # Parameters is a tag
        if key == "tag" or key == "tags":
            for tag in value.split(","):
                self.addTag(tag.strip())


    def getParameter(self, key, default=None):
        return self._parameters.get(key, default)
    
    def getAllParamters(self):
        return self._parameters.copy()

    def addTag(self, tag): # (str)
        self._tags.append(tag)

    def getTags(self):
        return self._tags
    
    def addCode(self, codeLanguage, codeSection):
        if type(codeSection) != list:
            raise Exception("Only list can be added as code section to Anki Question.")
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
        if self.getParameter("codeStyle", None) != None:
            fromattedString = highLightCode(codeString, codeLanguage, self.getParameter("codeStyle"))
        else:
            fromattedString = highLightCode(codeString, codeLanguage)
        return fromattedString
    
    def addNoteField(self, fieldName):
        namedField = NamedNoteField(fieldName)
        self._namedNoteFields[fieldName] = namedField
    
    def addLineToNamedField(self, fieldName, line):
        if self._namedNoteFields.get(fieldName, None) == None:
            self.addNoteField(fieldName)

        namedField = self._namedNoteFields.get(fieldName)
        namedField.addLine(line)
    
    def getNamedFields(self):
        return list(self._namedNoteFields.values())

    # String representation
    def __str__(self):
        return ("DeckName: {}. Question: {}. \nAsnwers: {}. \nTags: {}.\nComments: {}.\nParameters: {},\nMedia: {},\nCodeLanguage: {},\nCode: {}, NamedFields: {}").format(
            self.deckName, self.question, self.getAnswers(), self.getTags(), self.getComments(), self._parameters, self._media, self._codeLanguage, self._codeSection, self.getNamedFields())

    # Comparison to other questions
    def __eq__(self, other):
        if not isinstance(other, AnkiQuestion):
            return False

        return self.question == other.question and self.getAnswers() == other.getAnswers() and self.getTags() == other.getTags(
        ) and self.deckName == other.deckName and self.getComments() == other.getComments() and self._parameters == other._parameters and self.getMedia(
        ) == other.getMedia() and self.getCodeLanguage() == other.getCodeLanguage() and self.getCodeSection() == other.getCodeSection() and self.getNamedFields() == other.getNamedFields()

