
class NamedNoteField:

    def __init__(self, fieldName):
        self._fieldName = fieldName
        self._lines = []
    
    def addLine(self, line):
        self._lines.append(line)
    
    def getLines(self):
        return self._lines
    
    def getFieldName(self):
        return self._fieldName

    def __str__(self):
        return("fieldName: {}, lines: {}".format(self._fieldName, self._lines))
    
    def __eq__(self, other):
        if not isinstance(other, NamedNoteField):
            return False

        return (self.getFieldName()==other.getFieldName() and self.getLines() == other.getLines())