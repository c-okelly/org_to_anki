# org_to_anki

[![Build Status](https://travis-ci.org/c-okelly/org_to_anki.svg?branch=master)](https://travis-ci.org/c-okelly/org_to_anki) [![codecov](https://codecov.io/gh/c-okelly/org_to_anki/branch/master/graph/badge.svg)](https://codecov.io/gh/c-okelly/org_to_anki)

Python module to convert org or txt files into Anki question decks.

Provides two command line scripts. First is to upload an org or txt files to Anki. The second allow quick notetaking and storage.
 
Based on [AnkiConnect](https://ankiweb.net/shared/info/2055492159). An addon for Anki that provides a HTTP api for Anki.

## Contents

0. [Supported file type](#supported-file-type) 
1. [What is an org file](#what-is-an-org-file)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Comannd line scripts](#command-line-scripts)
5. [File syntax](#file-syntax)
6. [Parameters](#parameters)
7. [Running tests](#testing)
<!-- 8. [Debug mode](#debug-mode) -->
8. [Future features](#future-features)

## Supported file types

This project supports reading from both .org and .txt files. 

## What is an org file?

An org files a basic text file, very similar to .txt files. The file type is from Org Mode for Emacs but really you don't need to know much about this.

This is all you need to know for this project. 

* Asterisks ( * ) are used to to create bullet point style lists. 
* .org files are series of lists

* A list item for a question starts with *
* A list item for a answer starts with **
* A comment starts with a #

Examples are provided below.

This project will takes corretcly formated .org files and convert them to Anki cards.

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

## Requirements

1. Have the [Anki app](https://apps.ankiweb.net/) installed.
2. Installing the Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159).

	i. For OSX users of anki-connect see [note for OSX users](https://foosoft.net/projects/anki-connect/#installation)
	
	ii. For Windows users of anki-connect see [notes for Windows users](https://foosoft.net/projects/anki-connect/#installation) 

## Installation

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

### ankiq

* New questions are added to the default file stored at ~/orgNotes/quickOrgNotes.org
* This file is created by default if it does not already exist

```bash
ankiq
```
* Will start a Python input reply.
* Takes a questions and a series of anwers
* Empty line add a new question to the default org file

## File syntax

* Currently supports two different types of org or txt files
* All questions and answers should start with an asterix
* All comment lines start with a \#
```org
# Line comments
* Question
** Answer
```

* Each org file will be converted into its own deck in Anki

### Global Parameters 

* Parameters to be inherited by all questions / decks should be specified at the top file.
* These will be overwritten by parameters lower down the tree.

```org
# Basic Example
# type=Basic

* Question
** Answer
* Second Question
# type=Basic (and reversed card)
** Second Answer
```

### Basic org file syntax

* Sample answer and question in org or txt file

 ```org
 * What is the capital of Ireland?
 ** Dublin
 ```

* This will produce the following 1 Anki note in the same deck

```org
What is the capital of Ireland?
_______________________________________________________________________
Dublin
```
 
### Topics file syntax

* Each topic will be turned into its own subdeck. The name of this deck is given by the first line. E.G Capitals cities and Spoken languages.
* Allows for a group of related topics to be managed in a single file.

* Sample answer and questions for topics org or txt file.

 ```org
 #fileType = topics
 * Capital cities
 ** What is the capital of Ireland?
 *** Dublin
 * Spoken languages
 ** What are the main spoken languages in Ireland?
 *** English
 *** Irish
 ```

* This will produce the following 2 Anki note in separate decks

```org
What is the capital of Ireland?
_______________________________________________________________________
Dublin
```

```org
What are the main spoken languages in Ireland?
English
Irish
```

### Organised File syntax

* All topics are combined into the same deck to be uploaded to Anki

* In this case top level bullet points are used to organise the sub-questions. The top level are not part of any question. 

* Sample answer and questions for flatTopics org or txt file.

 ```org
 #fileType = organisedFile
* Chapter 1
** First main rule of scalability?
*** Each server behind load balancer
* Chapter 2
** What is the main purpose of the factory pattern?
*** Allow reference to objects via an interface
 ```

* This will produce the following 2 Anki notes in the same deck

```org
First main rule of scalability?
_______________________________________________________________________
Each server behind load balancer
```

```org
What is the main purpose of the factory pattern?
_______________________________________________________________________
Allow reference to objects via an interface
```

### FlatTopics file syntax

* All topics are combined into the same deck to be uploaded to Anki

* The name of each topic is added to the top of each card. An example is shown below

* Sample answer and questions for flatTopics org or txt file.

 ```org
 #fileType = flatTopics
 * Capital cities
 ** What is the capital of Ireland?
 *** Dublin
 * Spoken languages
 ** What are the main spoken languages in Ireland?
 *** English
 *** Irish
 ```

* This will produce the following 2 Anki notes in the same deck

```org
Capital Cities
What is the capital of Ireland?
_______________________________________________________________________
Dublin
```

```org
Spoken Languages
What are the main spoken languages in Ireland
_______________________________________________________________________
English
Irish
```

### OranisedFile syntax

* All topics are combined into the same deck to be uploaded to Anki

* In this case top level bullet points are used to organise the sub-questions. The top level are not part of any question. 

* Sample answer and questions for flatTopics org or txt file.

 ```org
 #fileType = organisedFile
* Chapter 1
** First main rule of scalability?
*** Each server behind load balancer
* Chapter 2
** What is the main purpose of the factory pattern?
*** Allow reference to objects via an interface
 ```

* This will produce the following 2 Anki notes in the same deck

```org
First main rule of scalability?
_______________________________________________________________________
Each server behind load balancer
```

```org
What is the main purpose of the factory pattern?
_______________________________________________________________________
Allow reference to objects via an interface
```

### Adding images

* You can add an image as one of your answers by correctly referancing as follows
	* Note: The image path should be relative to the file location
	* The file will name will not change on upload. 
		* In this case => "composite pattern.png"
		* This could lead to a conflict on Anki if files are named badly
* Check out the examples folder for a sample

```org
* What does the UML diagram for the compsite pattern look like?
** Image is displayed below
** [images_folder/composite pattern.png]
```

### Parameters

* Supported parameter syntax.

1. Each line must start with a hashtag
```org 
# type=Basic
# type = Basic
```

* Currently supported parameters are questions type

1. File type
* Org or txt files will default to type basic.
* If you want to use a topics layout this must be specified at the top of the file.

```org
# Comment line
# fileType=topics

* Topics 1
** Questions 1
*** Answer 1
```

2. Question type. Used to set the type of the Anki note.
    i. Default value is Basic

```org
# type=Basic
# type=Basic (and reversed card)
```

#### Parameter inheritance

* Questions and decks will inhert parameters from parent Decks
* Parameters inhereted will not override existing parameters.

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

## Debug mode

TODO: implement a debug mode
To activate debug 

## Future features

* Check to see if note exists before sending to Anki
* Expanded support for different paramters types
* If you have a feature you would like to see please open an issue!
 
