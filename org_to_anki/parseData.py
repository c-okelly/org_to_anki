# parse data into expected format
from AnkiQuestion import AnkiQuestion

def parse(fileName):

    file = open(fileName, "r")
    data = file.read().split('\n')
        
    # Sort data
    comments, questions, badFormatting = _sortData(data)
    # TODO bad formatting should be correctly logged
    
    # Turn raw questions into formated objects
    questions = _buildQuestions(questions)
    
    print(questions)
    return questions

def _buildQuestions(questions):

    # File identifer
    questionLine = 1
    answerLine = 2
    orgType = "basic"

    formatedQuestions = []
    currentQuestion = None

    for line in questions:
        noAstrics = line.split(' ')[0].count('*', 0, 10)
        line = _formatLine(line)

        if noAstrics == questionLine:
            # Store old question
            if currentQuestion != None:
                formatedQuestions.append(currentQuestion)
            # Next Question
            currentQuestion = AnkiQuestion(line)
        elif noAstrics == answerLine:
            currentQuestion.addAnswer(line)

    if currentQuestion != None:
        formatedQuestions.append(currentQuestion)
        currentQuestion = None

    return formatedQuestions

def _formatLine(line):

    line = " ".join(line.split(" ")[1:]) # Remove leading astrics
    line = line.capitalize()
    line = line.strip()

    return line

def _sortData(rawFileData):

    comments = []
    questions = []
    badFormatting = []

    for i in range(0,len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem[0]
            if firstLetter == "#":
                comments.append(currentItem)
            elif firstLetter == "*":
                questions.append(currentItem)
            else:
                badFormatting.append(["Line starts inccorectlly at line no " + i, currentItem])

    return (comments, questions, badFormatting)


                

if __name__ == "__main__":

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../tests/testData/basic.org')
    parse(fileName)