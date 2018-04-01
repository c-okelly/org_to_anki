
def convertCommentsToParameters(comments: [str]):

    parameters = {}
    for line in comments:
        parameters.update(convertLineToParamters(line))

    return parameters

def convertLineToParamters(line: str):

    parameters = {}
    line = line.strip()[line.count("#"):]
    pairs = line.split(",")
    for item in pairs:
        if "=" in item:
            item = item.strip()
            parts = item.split("=")
            parameters[parts[0].strip()] = parts[1].strip()

    return parameters