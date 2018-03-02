# org_to_anki

[![Build Status](https://travis-ci.org/c-okelly/org_to_anki.svg?branch=master)](https://travis-ci.org/c-okelly/org_to_anki) [![codecov](https://codecov.io/gh/c-okelly/org_to_anki/branch/master/graph/badge.svg)](https://codecov.io/gh/c-okelly/org_to_anki)

Basic Python moudle to convert org files into Anki question decks.

Will provide a number of command line utilties for uploading org files and add new notes to a preset org file.

Script works by parseing an org file and then using the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) AnkiConnect addon for Anki to upload the new questions.

Currently a work in progress. Aka it doesn't work! (yet)
Currently depends on a update to connect anki that has yet to be released.

## Requirements

1. Have Anki installed locally.
2. Have the following Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159) installed. 
    i. Ensure that the plugin is working correctly.

## Getting started

To install this module from source.

1. cd to the current module directory
2. python3 setup.py install

This will install 2 command line utilities to be used by the user as follows.

### org_to_anki

```bash
org_to_anki
```
* Will upload the defualt org file to Anki

```bash
org_to_anki /path/to/your/org/file.org
```
* Will upload the specified file to Anki

### ankiq

```bash
ankiq
```
* Will start Anki quick question builder. Takes question first and then a series of one line answers
* Give an empty answer to exit and save new question to the default org file.


## Org file syntax

* Each org file will be converted into its own deck in Anki
* Currently only a single layout type is supported.

### Basic org file structure

*Sample answer and question in org file*
 ```org
 * What is the capital of Ireland?
 ** Dublin
 ```
 
## Default values

1. Default url for ankiConnect is "http://127.0.0.1:8765/"
2. Default deck where all sub decks will be stored is Org Notes
3. Default folder for org files is ~/orgNotes/quickOrgNotes.org

 