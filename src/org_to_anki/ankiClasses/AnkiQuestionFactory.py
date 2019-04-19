from .AnkiQuestion import AnkiQuestion
from ..org_parser import DeckBuilderUtils
from ..org_parser import ParserUtils

class AnkiQuestionFactory:

    utils = DeckBuilderUtils.DeckBuilderUtils()

    def __init__(self, currentDeck, filePath, indentor = "*"):
        self.currentDeck = currentDeck
        self.filePath = filePath
        self.indentor = indentor
        self.currentQuestions = []
        self.currentAnswers = []
        self.currentComments = []
        self.questionsCreated = 0
        self.codeLanguage = None
        self.codeSection = []

    # Clear the current data
    def clearData(self):
        self.currentQuestions = []
        self.currentAnswers = []
        self.currentComments = []
        self.questionsCreated = 0
        self.codeLanguage = None
        self.codeSection = []

    def hasData(self):
        return len(self.currentQuestions) == 0 or len(self.currentAnswers) == 0 and len(self.currentComments) == 0

    def addAnswerLine(self, answer):
        self.currentAnswers.append(answer)

    def addQuestionLine(self, question):
        self.currentQuestions.append(question)

    def addCommentLine(self, comment):
        self.currentComments.append(comment)

    def addCode(self, codeLanguage, codeSection):
        if self.codeLanguage == None and len(self.codeSection) == 0:
            self.codeLanguage = codeLanguage
            self.codeSection = codeSection
        else:
            raise Exception("Only one code section per a question is supported.")

    ### Utility
    def questionHasAnswers(self):
        return len(self.currentAnswers) > 0 or len(self.codeSection) > 0

    # Build question based upon current data input
    # Should return an Question object
    def buildQuestion(self):

        newQuestion = AnkiQuestion()
        self.questionsCreated += 1

        # Add Question
        for line in self.currentQuestions:
            line = self.utils.removeAsterisk(line)
            line = self.utils.formatLine(line)
            newQuestion.addQuestion(line)

        # Add answers
        if len(self.currentAnswers) > 0: # Ignore adding question when codeSection is present
            noQuestionAsterisk = self.utils.countAsterisk(self.currentAnswers[0])
        while len(self.currentAnswers) > 0:
            line = self.currentAnswers.pop(0)
            noAsterisks = self.utils.countAsterisk(line)

            # Answer line
            if noAsterisks == noQuestionAsterisk:
                line = self.utils.removeAsterisk(line)
                line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                newQuestion.addAnswer(line)

            # Sublist in question
            elif noAsterisks > noQuestionAsterisk:

                subList = []
                subList.append(line)

                while len(self.currentAnswers) > 0 and self.utils.countAsterisk(self.currentAnswers[0]) > noQuestionAsterisk:
                    line = self.currentAnswers.pop(0)
                    line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                    subList.append(line)

                formatedSubList = self.utils.generateSublist(subList)
                newQuestion.addAnswer(formatedSubList)

            else:
                raise Exception("Line incorrectly processed.")

        # Add comments
        for comment in self.currentComments:
            newQuestion.addComment(comment)
            parameters = ParserUtils.convertLineToParameters(comment)
            for key in parameters.keys():
                newQuestion.addParameter(key, parameters.get(key))
        
        # Add code
        if self.codeSection != []:
            newQuestion.addCode(self.codeLanguage, self.codeSection)

        # Clear data and return
        self.clearData()

        print("Single question: " + str(self.questionsCreated))
        print("Question:", newQuestion.question)
        print("Answers:", newQuestion._answers)
        print()

        return newQuestion
