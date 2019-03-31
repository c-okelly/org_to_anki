# org_to_anki

[![Build Status](https://travis-ci.org/c-okelly/org_to_anki.svg?branch=master)](https://travis-ci.org/c-okelly/org_to_anki) [![codecov](https://codecov.io/gh/c-okelly/org_to_anki/branch/master/graph/badge.svg)](https://codecov.io/gh/c-okelly/org_to_anki)

Python module to convert org or txt files into Anki question decks.

Provides two command line scripts. First is to upload an org or txt files to Anki. The second allow quick notetaking and storage.
 
Based on [AnkiConnect](https://ankiweb.net/shared/info/2055492159). An addon for Anki that provides a HTTP api for Anki.

## Contents

0. [Supported file types](#supported-file-types) 
1. [What is an org file](#what-is-an-org-file)
2. [Using Org or text files](https://github.com/c-okelly/org_to_anki/blob/master/documentation/orgReadme.md)
3. [Using Word or LibreOffice files](https://github.com/c-okelly/org_to_anki/blob/master/documentation/docReadme.md) 
4. [Installation](#installation)
5. [Comand line scripts](#command-line-scripts)
6. [Running tests](#testing)
7. [Contributing](#contributing)

## Supported file types

This project supports reading from both .org, .txt, .docx (Word) and odt (LibreOffice) files. 

To use Word or LibreOffice files these must first be saved as HTML files. Please read the documentation on this.

## What is an org file?

An org files a basic text file, very similar to .txt files. The file type is from Org Mode for Emacs but really you don't need to know much about this.

This is all you need to know for this project. 

* Asterisks ( * ) are used to to create bullet point style lists. 
* .org files are series of lists

* A list item for a question starts with *
* A list item for a answer starts with **
* A comment starts with a #

Examples are provided below.


### Here is some example syntax for how question should be laid out

``` org
* Question
** Answer 1
** Answer 2
* Another Question
** Another answer
```

### More information on org-mode

Org mode is for keeping notes, maintaining TODO lists, planning projects, and authoring documents with a fast and effective plain-text system

[orgmode homepage](https://orgmode.org/)

## Org and Text files 

[Documentation on Org and Text files](https://github.com/c-okelly/org_to_anki/blob/master/documentation/orgReadme.md)

## LibreOffice and Word

[Documentation on LibreOffice or Word files](https://github.com/c-okelly/org_to_anki/blob/master/documentation/docReadme.md)


## Installation

### Requirements

1. Have the [Anki app](https://apps.ankiweb.net/) installed.
2. Installing the Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159).

	i. For OSX users of anki-connect see [note for OSX users](https://foosoft.net/projects/anki-connect/#installation)
	
	ii. For Windows users of anki-connect see [notes for Windows users](https://foosoft.net/projects/anki-connect/#installation) 

To install this module from source on Linux or OSx.

```bash
git clone https://github.com/c-okelly/org_to_anki
cd org_to_ani
python3 setup.py install
```

## Command line scripts

### org_to_anki

```bash
org_to_anki
```
* Upload the default org file to Anki

```bash
org_to_anki /path/to/your/org/file.org
```
* Upload the specified file to Anki



## Config values

* Config in project root contains all the default values for running
* Default org file is located at ~/orgNotes/quickOrgNotes.org
* Default anki-connect url is http://127.0.0.1:8765/

## Testing

A number of extra libraries are used in testing

* To run unittests 
``` bash
python3 setup.py nosetests
```

## Contributing 

All contributions are welcome. Please open a issue first to discuss your ideas!
4. [Using Word or LibreOffice files](#word-or-libreoffice-files) 
