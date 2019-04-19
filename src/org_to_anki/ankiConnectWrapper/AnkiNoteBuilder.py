from .. import config

class AnkiNoteBuilder:

    def __init__(self):
        self.defaultDeck = config.defaultDeck

    def buildNote(self, ankiQuestion):

        # All decks stored under default deck
        if ankiQuestion.deckName == "" or ankiQuestion.deckName is None:
            # TODO log note was built on default deck
            deckName = self.defaultDeck
        else:
            deckName = self._getFullDeckPath(ankiQuestion.deckName)

        # TODO: Verify model name correctly and use parameters
        # Defaults to basic type by default
        modelName = ankiQuestion.getParameter("noteType", "Basic")

        # Legacy support to note types
        if ankiQuestion.getParameter("type") is not None:
            modelName = ankiQuestion.getParameter("type")

        note = {"deckName": deckName, "modelName": modelName}
        note["tags"] = ankiQuestion.getTags()

        # formattedQuestion = [ankiQuestion.getFormattedCodeSection()]
        # Generate fields
        fields = {}
        fields["Front"] = self.createQuestionString(ankiQuestion.getAllParamters(), ankiQuestion.getQuestions())
        fields["Back"] = self.createAnswerString(ankiQuestion.getAllParamters(), ankiQuestion.getAnswers())

        note["fields"] = fields
        return note

    def createQuestionString(self, ankiParamters, questions):

        if len(questions) == 1:
            question =  questions[0].replace("\n", "<br>")
            return question
        else:
            questionString = ""
            for q in questions:
                q = self._formatString(q)
                q = q.strip().replace("\n", "<br>")
                questionString += q + " <br>"
            return questionString
            

    def createAnswerString(self, ankiParamters, answers):

        answerString = ""

        # Check for list type
        listType = ankiParamters.get("list", "unordered").lower()

        
        if listType == "false" or listType == "none": 
            for i in answers:
                i = self._formatString(i)
                answerString += i + "<br>"  # HTML link break
            return answerString
        
        listTag = "ul" # Default option

        if listType == "unordered" or listType == "ul":
            listTag = "ul"
        elif listType == "ordered" or listType == "ol":
            listTag = "ol"

        # Only create list if answers exits
        if len(answers) > 0:
            # Can only can create single level of indentation. Align bulletpoints
            answerString += "<{} style='list-style-position: inside;'>".format(listTag)
            for i in answers:
                i = self._formatString(i)
                if isinstance(i, str):
                    answerString += "<li>" + i + "</li>"
                elif isinstance(i, list):
                    answerString += self.createAnswerString(ankiParamters, i)
                else:
                    raise Exception("Unsupported action with answer string from => " + str(i))

            answerString += "</{}>".format(listTag)

        return answerString

    def _getFullDeckPath(self, deckName): # (str)
        return str(self.defaultDeck + "::" + deckName)

    def _formatString(self, unformattedString):

        return unformattedString