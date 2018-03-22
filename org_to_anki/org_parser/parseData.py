# parse data into expected format
from ..ankiClasses.AnkiDeck import AnkiDeck
from .DeckBuilder import DeckBuilder


def parse(filePath: str) -> ([AnkiDeck]):

    deckBuilder = DeckBuilder()

    data = _formatFile(filePath)
    fileName = filePath.split("/")[-1].split(".")[0]

    comments, content, badFormatting = _sortData(data)
    # TODO bad formatting should be correctly logged

    globalParameters = _convertCommentsToParameters(comments)
    fileType = globalParameters.get("fileType", "basic")

    deck = deckBuilder.buildDeck(content, fileName, fileType)
    # deck = _buildQuestions(content, fileName, fileType)

    return deck


def _formatFile(filePath: str):

    file = open(filePath, "r")
    data = file.read().split('\n')

    return data


def _convertCommentsToParameters(comments: [str]):

    parameters = {}
    for line in comments:
        line = line.strip()[line.count("#"):]
        pairs = line.split(",")
        for item in pairs:
            if "=" in item:
                item = item.strip()
                parts = item.split("=")
                parameters[parts[0].strip()] = parts[1].strip()

    return parameters


def _sortData(rawFileData: [str]) -> ([str], [str], [str]):

    comments, questions, badFormatting = [], [], []

    for i in range(0, len(rawFileData)):
        currentItem = rawFileData[i]
        if len(currentItem) > 0:
            firstLetter = currentItem.strip()[0]
            if firstLetter == "#":
                comments.append(currentItem)
            elif firstLetter == "*":
                questions.append(currentItem)
            else:
                badFormatting.append(
                    ["Line starts incorrectly at line no " + str(i) + ". " + currentItem])

    return (comments, questions, badFormatting)


if __name__ == "__main__":

    # dir = os.path.dirname(__file__)
    # filePath = os.path.join(dir, '../tests/testData/basic.org')
    # questions = parse(filePath)
    # print(questions[0])

    x = _convertCommentsToParameters(
        ["#fileType=basic, secondArg=10", "##file=basic"])
    print(x)
