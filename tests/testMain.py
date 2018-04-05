import sys
sys.path.append('../org_to_anki')
from unittest.mock import patch

from org_to_anki.main import _getUploadFilePath
from org_to_anki import config

def testGetUploadFilePathWithNoSysArgs():

    expectedFilePath = config.quickNotesOrgPath
    testArgs = ['/usr/local/bin/org_to_anki'] 
    with patch.object(sys, 'argv', testArgs):
        filePath = _getUploadFilePath()
        assert(filePath == expectedFilePath)

def testGetUploadFilePathWithSysArgs():

    expectedFilePath = 'test/path/to.org'
    testArgs = ['/usr/local/bin/org_to_anki', expectedFilePath] 
    with patch.object(sys, 'argv', testArgs):
        filePath = _getUploadFilePath()
        assert(filePath == expectedFilePath)







