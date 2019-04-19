import sys
sys.path.append('../org_to_anki')

from org_to_anki.converters.codeHighlighter import highLightCode

def testCodeHighlightingWithMultipleLines():

    unformattedCode= """print("Hello World!)"\n\nif(True):\n  print("indent") """
    expectedCode = """<div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello World!)&quot;</span><br><br><span style="color: #008800; font-weight: bold">if</span>(<span style="color: #008800; font-weight: bold">True</span>):<br>  <span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;indent&quot;</span>) <br></pre></div> </div>"""

    formattedCode = highLightCode(unformattedCode, "python3")

    assert(formattedCode == expectedCode)

def testCodeHighlightingWithColorfulStyle():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """<div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello World!)&quot;</span> <br></pre></div> </div>"""

    formattedCode = highLightCode(unformattedCode, "python3")

    assert(formattedCode == expectedCode)

def testCodeHighlightingWithManniStyle():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """<div style="text-align:left"> <div class="highlight" style="background: #f0f3f3"><pre style="line-height: 125%"><span></span><span style="color: #336666">print</span>(<span style="color: #CC3300">&quot;Hello World!)&quot;</span> <br></pre></div> </div>"""

    formattedCode = highLightCode(unformattedCode, "python3", "manni")

    assert(formattedCode == expectedCode)

def testCodeFailsWithUnknownLanguage():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """print("Hello World!)" \nWas unable to find a suitable Lexor for phrase: xyz"""

    formattedCode = highLightCode(unformattedCode, "xyz")

    assert(formattedCode == expectedCode)

def testCodeWithUnknownStyleDefaultsToColourful():

    unformattedCode= """print("Hello World!)" """
    expectedCode = """<div style="text-align:left"> <div class="highlight" style="background: #ffffff"><pre style="line-height: 125%"><span></span><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello World!)&quot;</span> <br></pre></div> </div>"""

    formattedCode = highLightCode(unformattedCode, "python3", "xyz")

    assert(formattedCode == expectedCode)

