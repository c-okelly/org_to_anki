
from ..ankiClasses.AnkiQuestion import AnkiQuestion
from ..ankiClasses.AnkiDeck import AnkiDeck


class DeckBuilder:

    def buildDeck(self, questions: [str], deckName: str, fileType: str='basic'):

        if fileType == 'basic':
            deck = self._buildBasicDeck(questions, deckName)
        else:
            raise Exception('Unsupported file type: ' + fileType)
        
        return deck


    def _buildBasicDeck(self, questions, deckName):

        questionLine = 1
        answerLine = 2

        deck = AnkiDeck(deckName)
        currentQuestion = None

        for line in questions:
            noAstrics = line.split(' ')[0].count('*', 0, 10)
            # TODO lines of differnt type need different formatting

            if noAstrics == questionLine:
                line = " ".join(line.split(" ")[1:])
                # Store old question
                if currentQuestion is not None:
                    deck.addQuestion(currentQuestion)
                # Next Question
                currentQuestion = AnkiQuestion(line, deckName)

            elif noAstrics == answerLine:
                line = " ".join(line.split(" ")[1:])
                currentQuestion.addAnswer(line)

            # Sublist in question
            elif noAstrics > answerLine:
                # Remove answer astrics
                line = line.strip().split(" ")
                line[0] = line[0][answerLine:]
                line = " ".join(line)
                currentQuestion.addAnswer(line)

            else:
                raise Exception("Line incorrectly processed.")

        if currentQuestion is not None:
            deck.addQuestion(currentQuestion)
            currentQuestion = None

        return deck
