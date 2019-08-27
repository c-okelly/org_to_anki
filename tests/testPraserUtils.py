import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import ParserUtils 

def testConvertCommentsToParameters():

    comments = ["#fileType=basic, secondArg=10", "##file=basic", "#fileType2 = topics"]
    result = ParserUtils.convertCommentsToParameters(comments)
    expected = {'fileType': 'basic', 'secondArg': '10', 'file': 'basic', 'fileType2': 'topics'}
    assert(result == expected)

def testConvertLineToParameter():

    assert(ParserUtils.convertLineToParameters("type=Basic") == {'type' : 'Basic'})
    assert(ParserUtils.convertLineToParameters("#type=Basic, type2=2") == {'type' : 'Basic', 'type2':'2'})
    assert(ParserUtils.convertLineToParameters("type = Basic") == {'type' : 'Basic'})
    assert(ParserUtils.convertLineToParameters("#type = Basic") == {'type' : 'Basic'})
    assert(ParserUtils.convertLineToParameters("# type = Basic") == {'type' : 'Basic'})
    assert(ParserUtils.convertLineToParameters("# type = Basic (and reversed card), sec=1") == {'type' : 'Basic (and reversed card)', 'sec':'1'})

def testMultipleParameters():

    line = "#type0=a, type1=b, type2=c"
    data = ParserUtils.convertLineToParameters(line)

    assert(data == {'type0': 'a', 'type1': 'b', 'type2': 'c'})

def testEmptyLine():

    line = "# Only a commnet! No data"
    data = ParserUtils.convertLineToParameters(line)

    assert(data == {})


def testCommaSeperatedDataForTags():

    data = ParserUtils.convertLineToParameters("# tags=a, b, c")
    assert(data == {'tags': 'a, b, c'})

    data = ParserUtils.convertLineToParameters("# tag=a, tag=b, tag=c")
    assert(data == {'tag': 'a,b,c'})