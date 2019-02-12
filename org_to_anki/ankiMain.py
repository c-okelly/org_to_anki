# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from aqt.importing import ImportDialog

from main import parseAndUploadOrgFile

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def importNewFile():

    # show a message box
    # showInfo("Card count: %d. Wowo this really worked did it?" % cardCount)
    d = QFileDialog(mw)
    filePath = d.getOpenFileName()
    showInfo(filePath)

    ## Do real main
    parseAndUploadOrgFile(filePath, embedded=True)


# create a new menu item, "test"
action = QAction("Import Org File", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(importNewFile)
# and add it to the tools menu
mw.form.menuTools.addAction(action)