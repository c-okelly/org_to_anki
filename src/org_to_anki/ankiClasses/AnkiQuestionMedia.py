class AnkiQuestionMedia:

    def __init__(self, mediaType, fileName, data):
        self.mediaType = mediaType
        self.fileName = fileName
        self.data = data

    def __str__(self):
        return ("Media data for file type: %s and name %s") % (self.mediaType, self.fileName)
    
    def __eq__(self, other):
        return self.mediaType == other.mediaType and self.fileName == other.fileName and self.data == other.data

