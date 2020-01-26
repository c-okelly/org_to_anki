import sys
sys.path.append('../src/org_to_anki')

from org_to_anki.noteModels.models import NoteModels


def testNodeModelsCanBeLoaded():

    models = NoteModels()

    assert(models.getBasicModel().get("name") == "Basic")
    assert(models.getRevseredModel().get("name") == "Basic (and reversed card)")
    assert(models.getClozeModel().get("name") == "Cloze")