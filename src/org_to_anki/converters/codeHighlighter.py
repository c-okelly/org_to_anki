import sys
try:
    from .consts import *  # import addon_path
    #always use shipped pygments library
    sys.path.insert(0, os.path.join(addon_path, "../libs"))
except:
    sys.path.insert(0, "../libs")

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
        formatter = HtmlFormatter(style=style, noclasses=True)
    except:
        errorMessage = "Was unable to find a suitable Style for phrase: {}".format(style)
        return code + "\n" + errorMessage


    formattedCode = highlight(code, lexer, formatter)

    return formattedCode.replace("\n", "")