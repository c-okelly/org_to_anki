
import json

class NoteModels:


    def getBasicModel(self):
        basic =  r"""
        {
            "name": "Basic",
            "inOrderFields": ["Front", "Back"],
            "cardTemplates": [
                {
                    "Front": "{{Front}}",
                    "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
                }
            ],
            "css" : ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n"
        }
        """

        return json.loads(basic)

    def getRevseredModel(self):

        reversed = r"""
        {
            "name": "Basic (and reversed card)",
            "inOrderFields": ["Front", "Back"],
            "cardTemplates":  [
                {
                    "Front": "{{Front}}",
                    "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
                },
                {
                    "Front": "{{Back}}",
                    "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}"
                }
            ],
            "css" : ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n"
        }
        """

        return json.loads(reversed)

    def getClozeModel(self):

        cloze = r"""
        {
            "name": "Cloze",
            "inOrderFields": ["Text", "Extra"],
            "cardTemplates": [
                {
                    "Front": "{{cloze:Text}}",
                    "Back": "{{cloze:Text}}<br>\n{{Extra}}"
                }
            ],
            "css" : ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n.cloze {\n font-weight: bold;\n color: blue;\n}\n.nightMode .cloze {\n color: lightblue;\n}"
        }
        """

        return json.loads(cloze)


