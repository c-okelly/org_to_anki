
def convertCommentsToParameters(comments): # ([str])

    parameters = {}
    for line in comments:
        parameters.update(convertLineToParameters(line))

    return parameters


def convertLineToParameters(line): # str

    parameters = {}
    line = line.strip()[line.count("#"):]
    pairs = line.split(",")
    for item in pairs:
        if "=" in item:
            item = item.strip()
            parts = item.split("=")
            # TODO: Make lowercase parameters
            parameters[parts[0].strip()] = parts[1].strip()

    return parameters

# def validGlobalParameter(key, value):

#     if key == "type" or key == "noteType":
#         if 
#     else:
#         return True