from .AnkiQuestion import AnkiQuestion
from ..org_parser import DeckBuilderUtils
from ..org_parser import ParserUtils

class AnkiQuestionFactory:

    utils = DeckBuilderUtils.DeckBuilderUtils()

    def __init__(self, currentDeck, filePath, indentor = "*"):
        self.currentDeck = currentDeck
        self.filePath = filePath
        self.indentor = indentor
        self.curentQuestions = []
        self.currentAnswers = []
        self.currentComments = []
    
    # Clear the current data
    def clearData(self):
        self.curentQuestions = []
        self.currentAnswers = []
        self.currentComments = []

    def hasData(self):
        return len(self.curentQuestions) == 0 or len(self.currentAnswers) == 0 and len(self.currentComments) == 0

    def addAnswerLine(self, answer):
        self.currentAnswers.append(answer)

    def addQuestionLine(self, question):
        self.curentQuestions.append(question)

    def addCommentLine(self, comment):
        self.currentComments.append(comment)

    ### Utility
    def questionHasAnswers(self):
        return len(self.currentAnswers) > 0

    # Build question based upon current data input
    # Should return an Question object
    def buildQuestion(self):

        newQuestion = AnkiQuestion()

        # Add Question
        for line in self.curentQuestions:
            line = self.utils.removeAstrics(line)
            line = self.utils.formatLine(line)
            newQuestion.addQuestion(line)

        # Add answers
        noQuestionAstrics = self.utils.countAstrics(self.currentAnswers[0])
        while len(self.currentAnswers) > 0:
            line = self.currentAnswers.pop(0)
            noAstrics = self.utils.countAstrics(line)

            # Asnwer line
            if noAstrics == noQuestionAstrics:
                line = self.utils.removeAstrics(line)
                line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                newQuestion.addAnswer(line)

            # Sublist in question
            elif noAstrics > noQuestionAstrics:

                subList = []
                subList.append(line)

                while len(self.currentAnswers) > 0 and self.utils.countAstrics(self.currentAnswers[0]) > noQuestionAstrics:
                    line = self.currentAnswers.pop(0)
                    line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                    subList.append(line)

                formatedSubList = self.utils.generateSublist(subList)
                newQuestion.addAnswer(formatedSubList)

            else:
                raise Exception("Line incorrectly processed.")

        for comment in self.currentComments:
            newQuestion.addComment(comment)
            parameters = ParserUtils.convertLineToParamters(comment)
            for key in parameters.keys():
                newQuestion.addParameter(key, parameters.get(key))

        # Clear data and return
        self.clearData()

        return newQuestion
