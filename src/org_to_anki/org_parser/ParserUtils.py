
# Get Anki sync or urllib2
try:
    from anki.sync import AnkiRequestsClient
    anki = "set"
except:
    anki = None
    import requests

    
def getImageFromUrl(url):

    if anki == "set":
        client = AnkiRequestsClient()
        client.timeout = URL_TIMEOUT
        resp = client.get(url)
        content = client.streamContent(resp)
    else:
        resp = requests.get(url)
        content = resp.content

    return content

def convertCommentsToParameters(comments): # ([str])

    parameters = {}
    for line in comments:
        parameters.update(convertLineToParameters(line))

    return parameters


def convertLineToParameters(line): # str

    parameters = {}
    line = line.strip()[line.count("#"):]


    # Return if no paramters
    if "=" not in line:
        return {}

    pairs = line.split(",")

    # Rejoin pairs based upon equals signed
    # This is for comma seperated lists
    formattedPairs = []
    for i in pairs:
        if "=" not in i:
            formattedPairs[-1] += "," + i
        else:
            formattedPairs.append(i)

    for item in formattedPairs:
        if "=" in item:
            item = item.strip()
            parts = item.split("=")
            key = parts[0].strip()
            value = parts[1].strip()

            # TODO: Make value lowercase parameters
            if key in parameters:
                parameters[key] = parameters[key] + "," + value
            else:
                parameters[key] = value

    return parameters

# def validGlobalParameter(key, value):

#     if key == "type" or key == "noteType":
#         if 
#     else:
#         return True