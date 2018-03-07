import sys
sys.path.append('../org_to_anki')
import os

from org_to_anki.quickNote import writeQuickNote
from org_to_anki.ankiClasses import AnkiQuestion
from org_to_anki.utils import createQuickNotesFile

def test_Quick_Note_Writer():
    dir = os.path.dirname(__file__)
    dirPath = dir + "/" + "orgNotes"
    filePath = dirPath + "/" + "quickOrgNotes.org"
    createQuickNotesFile(dirPath)

    # assert(os.path.exists(dirPath) == True)
    # Build question
    q = "* What is the capital of Ireland?\n** Dublin\n"
    writeQuickNote(q, filePath)
    with open(filePath, "r") as orgFile:
        content = orgFile.read()
    
    assert(q == content)
    os.remove(filePath)
    os.rmdir(dirPath)
    

