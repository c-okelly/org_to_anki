# org_to_anki

[![Build Status](https://travis-ci.org/c-okelly/org_to_anki.svg?branch=master)](https://travis-ci.org/c-okelly/org_to_anki) [![codecov](https://codecov.io/gh/c-okelly/org_to_anki/branch/master/graph/badge.svg)](https://codecov.io/gh/c-okelly/org_to_anki)

Python moudle to convert org files into Anki question decks.

Provides two command line scripts to upload org files and take new basic notes quickly.
 
Based on [AnkiConnect](https://ankiweb.net/shared/info/2055492159)an addon for Anki that provides a HTTP api for Anki.

## Contents

1. Requirements
2. Installation
3. Comannd line scripts
4. Org file syntax
5. Default values
6. Running tests
7. Future features

## Requirements

1. Have Anki app installed.
2. Installing the Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159). 
    i. For OSX users of anki-connect see [note for OSX users](https://foosoft.net/projects/anki-connect/#installation)
    ii. For Windows usersa of anki-connect see [notes for Windows users](https://foosoft.net/projects/anki-connect/#installation) 

## Installation

To install this module from source.

1. cd into the module directory
2. python3 setup.py install

## Comannd line scripts

### org_to_anki

```bash
org_to_anki
```
* Upload the defualt org file to Anki

```bash
org_to_anki /path/to/your/org/file.org
```
* Upload the specified file to Anki

### ankiq

* New questions are added to the default file stored at ~/orgNotes/quickOrgNotes.org
* This file is created by default if it does not already exist

```bash
ankiq
```
* Will start a Python input reply.
* Takes a questions and a series of anwers
* Empty line add a new question to the default org file

## Org file syntax

* Currently supports two differnt types of org files
* All questions and answers should start with astrics
* All comment lines start with a #

* Each org file will be converted into its own deck in Anki
* Currently only a single layout type is supported.

### Basic org file syntax

* Sample answer and question in org file

 ```org
 * What is the capital of Ireland?
 ** Dublin
 ```
 
### Topics file syntax

* Each topic will be turned into it's own subdeck. Allows for a group of related topics to be managed in a single file.

* Sample answer and questions for topics org file.

 ```org
 * Capital cities
 ** What is the capital of Ireland?
 *** Dublin
 * Spoken languages
 ** What are the main spoken languages in Ireland?
 *** English
 *** Irish
 ```

### Parameters

* Supported parameter syntax.

1. Each line must start with a #
2. # type=Basic
3. # type = Basic

* Currently supported parameters are questions type

1. Question type. Used to set the type of the Anki note.
    i. Default value is Basic

```org
# type=Basic
# type=Basic (and reversed card)
```

* Parameter inheritance

1. Paramaters are inherited from Decks and parent Decks

## Config values

* Config contains all the default values for setup
* Default org files ~/orgNotes/quickOrgNotes.org
* Default anki url is http://127.0.0.1:8765/

## Testing

A number of extra libraries are used in testing

* To run unittests 
``` bash
python3 setup.py nosetests
```

## Future features

* Check to see if note exists before sendin to Anki
* Expanded support for different paramters types
 
