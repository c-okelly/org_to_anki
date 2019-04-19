import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../org_to_anki/libs"))

from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

def highLightCode(code, language, style="colorful"):

    # Replace non break white space if exists
    code = code.replace('\u00A0', ' ')

    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound as e:
        errorMessage = "Was unable to find a suitable Lexor for phrase: {}".format(language)
        return code + "\n" + errorMessage
    
    try:
        formatter = HtmlFormatter(style=style, noclasses=True, lineseparator="<br>")
    except:
        # TODO => Error is getting buried here and reverting to default style
        errorMessage = "Was unable to find a suitable Style for phrase: {}. Falling back to colorful style.".format(style)
        formatter = HtmlFormatter(style="colorful", noclasses=True, lineseparator="<br>")
        print(errorMessage)


    formattedCode = highlight(code, lexer, formatter)

    # Ensure code is always aligned
    formattedCode = """<div style="text-align:left"> {} </div>""".format(formattedCode)

    return formattedCode.replace("\n", "")