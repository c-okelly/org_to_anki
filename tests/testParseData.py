from org_to_anki import parseData, AnkiQuestion
import os

def test_basic_parseData():

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'testData/basic.org')
    actualQuestion = parseData.parse(filename)[0]

    expectedQuestion = AnkiQuestion.AnkiQuestion("Put request", "basic")
    expectedQuestion.addAnswer("Puts file / resource at specific url")
    expectedQuestion.addAnswer("If file ==> exists => replaces // !exist => creates")
    expectedQuestion.addAnswer("Request => idempotent")

    assert actualQuestion == expectedQuestion