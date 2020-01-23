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

    # Whitespace test
    data = ParserUtils.convertLineToParameters("# tags=a something, b, c")
    assert(data == {'tags': 'a something, b, c'})

    data = ParserUtils.convertLineToParameters("# tag=a, tag=b, tag=c")
    assert(data == {'tag': 'a,b,c'})


def test_getImageFromUrl_CommandLineMode():

    googleDocsImageUrl = "https://lh3.googleusercontent.com/gdEMfGtrSRTvbTiXwysYJ_5XxqieWt0Z9vtFw0jQxOlbjo43_PJYa4kCusZjmkbe_euwGa4KAWEo2xJvEzHkwIpVN3H-XvCxVXCpQNOcH9_tERcVodYf75t18hYlargfKgYtHYvM"

    imageData = ParserUtils.getImageFromUrl(googleDocsImageUrl)

    # Poor way to assert an image
    assert(len(imageData) == 68035)