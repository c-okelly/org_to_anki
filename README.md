# org_to_anki

Basic Python script to convert org files into Anki question decks.

Script works by parseing an org file and then using the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) AnkiConnbct addon for Anki to upload the new questions.

Currenly a work in progress. Aka it doesn't work! (yet)

# Requirements

1. Have Anki installed locally.
2. Have the following Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159) 

# Getting started

To install this script.

1. cd to the current module directory
2. run $"pip3 install -e ."

# Defaults 

1. Default url for ankiConnect is "http://127.0.0.1:8765/"
2. Default deck where all sub decks will be stored is Org Notes
3. Default folder for org files is orgNotes/

# Correctly structuring the Org file

* Each org file will be converted into its own deck in Anki
* Basic version will only support a single list of questions per an org file

* Format is as follows for a basic question

*Sample answer and question in org file*
 ```org
 * What is the capital of Ireland?
 ** Dublin
 ```
 