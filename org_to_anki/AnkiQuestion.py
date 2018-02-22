class AnkiQuestion:

    def __init__(self, question):
        self.topic = ""
        self.tags = []
        self.question = question
        self.answers = []

    def addAnswer(self, answer):
        self.answers.append(answer)

    def __str__(self):
        return "Question: %s. \nAsnwers: %s. \nTags: %s" % (self.question, self.answers, self.tags)
    
    def __eq__(self, other):
        # TODO compare all properties
        return self.question == other.question and self.answers == other.answers 