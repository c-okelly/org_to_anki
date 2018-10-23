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