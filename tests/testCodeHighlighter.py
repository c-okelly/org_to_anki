import sys
sys.path.append('../org_to_anki')

from org_to_anki.converters.codeHighlighter import highLightCode


def testCodeHighlightingWithColorfulStyle():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello World!)&quot;</span> </pre></div>"""

    formattedCode = highLightCode(unformattedCode, "python3")

    assert(formattedCode == expectedCode)

def testCodeHighlightingWithManniStyle():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """<div class="highlight" style="background: #f0f3f3"><pre style="line-height: 125%"><span></span><span style="color: #336666">print</span>(<span style="color: #CC3300">&quot;Hello World!)&quot;</span> </pre></div>"""

    formattedCode = highLightCode(unformattedCode, "python3", "manni")

    print(formattedCode)
    assert(formattedCode == expectedCode)

def testCodeFailsWithUnknownLanguage():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """print("Hello World!)" \nWas unable to find a suitable Lexor for phrase: xyz"""

    formattedCode = highLightCode(unformattedCode, "xyz")

    assert(formattedCode == expectedCode)

def testCodeFailsWithUnknownStyle():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """print("Hello World!)" \nWas unable to find a suitable Style for phrase: xyz"""

    formattedCode = highLightCode(unformattedCode, "python3", "xyz")

    print(formattedCode)
    assert(formattedCode == expectedCode)

