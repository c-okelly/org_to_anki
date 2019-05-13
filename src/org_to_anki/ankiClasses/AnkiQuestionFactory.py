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
        self.parameters = {}

    # Clear the current data
    def clearData(self):
        self.currentQuestions = []
        self.currentAnswers = []
        self.currentComments = []
        self.questionsCreated = 0
        self.codeLanguage = None
        self.codeSection = []
        self.parameters = {}

    def hasData(self):
        return len(self.currentQuestions) == 0 or len(self.currentAnswers) == 0 and len(self.currentComments) == 0

    def addAnswerLine(self, line, metadata={}):
        # Check for answers for other fields
        metadata = dict(metadata)
        self.currentAnswers.append({"line":line, "metadata":metadata})

    def addQuestionLine(self, question):
        self.currentQuestions.append(question)

    def addCommentLine(self, comment):
        self.currentComments.append(comment)
        parameters = ParserUtils.convertLineToParameters(comment)
        for key in parameters.keys():
            self.parameters[key] = parameters.get(key)

    def addCode(self, codeLanguage, codeSection):
        if self.codeLanguage == None and len(self.codeSection) == 0:
            self.codeLanguage = codeLanguage
            self.codeSection = codeSection
        else:
            raise Exception("Only one code section per a question is supported.")

    ### Utility
    def isValidQuestion(self):
        # Check for one of following three conditions
        # 1. Has answers
        # 2. Has a code section
        # 3. Has card type cloze 
        return len(self.currentAnswers) > 0 or len(self.codeSection) > 0 or self.parameters.get("type") == "Cloze" or self.parameters.get("type") == "Cloze" 

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
        noQuestionAsterisk = None
        if len(self.currentAnswers) > 0: # Ignore adding question when codeSection is present
            noQuestionAsterisk = self.utils.countAsterisk(self.currentAnswers[0].get("line"))


        # TODO refactor to take into account metadata
        self.addAnswerToNewQuestion(self.currentAnswers, newQuestion, noQuestionAsterisk)

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

        # print("Single question: " + str(self.questionsCreated))
        # print("Question: {}".format(newQuestion.question))
        # print("Answers: {}".format(newQuestion._answers))
        # print("Fields: {}".format(newQuestion.getNamedFields()))
        # print()

        return newQuestion
    
    def addAnswerToNewQuestion(self, answers, newQuestion, noQuestionAsterisk):
        
        # newAnswers = []
        # for answer in answers:
        #     newAnswers.append(answer.get("line"))
            
        # answers = newAnswers


        while len(answers) > 0:
            dataLine = answers.pop(0)
            line = dataLine.get("line")
            fieldName = dataLine.get("metadata").get("fieldName", None)

            noAsterisks = self.utils.countAsterisk(line)

            # Answer line
            if noAsterisks == noQuestionAsterisk:
                line = self.utils.removeAsterisk(line)
                line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                newQuestion.addAnswer(line, fieldName)

            # Sublist in question
            elif noAsterisks > noQuestionAsterisk:

                subList = []
                subList.append(line)

                while len(answers) > 0 and self.utils.countAsterisk(answers[0].get("line")) > noQuestionAsterisk:
                    dataLine= answers.pop(0)
                    line = dataLine.get("line")
                    fieldName = dataLine.get("metadata").get("fieldName", None)

                    line = self.utils.parseAnswerLine(line, self.filePath, newQuestion)
                    subList.append(line)

                formatedSubList = self.utils.generateSublist(subList)
                newQuestion.addAnswer(formatedSubList, fieldName)

            else:
                raise Exception("Line incorrectly processed.")

