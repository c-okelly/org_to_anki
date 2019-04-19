
# Word or LibreOffice files

1. [File syntax](#File-syntax) 
2. [Saving files](#Saving-Word-or-LibreOffice-files) 
3. [Supported parameters](#Supported-parameters) 
4. [HTML code and LaTeX](#html-code-and-latex)

## Microsoft Word support

Currently Microsoft Word is partially supported. I am experianced a number of bugs from users and working to get back to full support. In the mean time I would advice users to use [LibreOffce](https://www.libreoffice.org/) instead. This is free, open source.


## File syntax

Word and LibreOffice files are now support using bulletpoints for the question answers.

Instead of using * or ** you can use bulletpoint list instead. All other syntax rules apply.

Format of question ansewers

* What is the capital of Ireland

	`# type = basic`
	* Dublin
* What is the capital of Germany
	* Berlin
	
## Multi-level files

Question with sublists are also currently supported. Example below:

* A question
	* Group 1
		* Item A
		* Item B
	* Group 2
		* Item C
		* Item D


## Saving Word or LibreOffice files 

In order to parse Word or LibreOffice files these must first be saved as HTML / HTM files. Unsaved examples are both located in `exampleLibreOfficeAndWordFiles` folder.

Saving a Word file
```
File > Save As
```
For "File Format" select "Web Page (.htm)"

Saving a LibreOffice file
```
File > Save As
```
For "File type" select "HTML Document (.html)"

### Basic example

![Basic Libre Office Example](../gifs/Basic_LibreOffice_Example.gif)


## File types for organisation

Users may want to organise their files in a specific ways. 

Currently five differnet file types are supported.

* [Basic file types (Default)](#basic-org-file-syntax)
* [Topics file type](#topics-file-syntax)
* [Organised file type](#Organised-File-syntax)
* [FlatTopics file type](#FlatTopics-file-syntax)
* [OrganisedFlatFile file type](#OrganisedFlatFile-file-syntax)

### Basic org file syntax

* Sample answer and question in org or txt file
* This is the default

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

* Each topic will be turned into its own subdeck. 
    * The name of this deck is given by the first line. E.G Capitals cities and Spoken languages.
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
_______________________________________________________________________
English
Irish
```

### Organised File syntax

* All topics are combined into the same deck to be uploaded to Anki
    * Top level bullet points are ignored
    * Normally used as metadata the user has to organise the information

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
    * The name of each topic is added to the top of each card.
    * Allows user to include general data in each question

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

### OrganisedFlatFile file syntax

 * All topics are combined into the same deck to be uploaded to Anki
    * First level bullet points are added as metadata to each question
    * The second level of bullet points are used for data organisation and are ignored

 * Sample answer and questions for flatTopics org or txt file.

```org
 #fileType = organisedFlatFile

* Systems design primer
** Scalability intro blog
*** First main rule of scalability?
**** Each server behind load balancer

* Programming design patterns (online version)
** Factory pattern
*** What is the main purpose of the factory pattern? (2)
**** To allow object creation without exposing the creation logic to client
**** Allow reference to objects via an interface
```

 * This will produce the following 2 Anki notes in the same deck

```org
Systems design primer
First main rule of scalability?
_______________________________________________________________________
Dublin
```

```org
Programming design patterns (online version)
What is the main purpose of the factory pattern? (2)
_______________________________________________________________________
To allow object creation without exposing the creation logic to client
Allow reference to objects via an interface
```
## Adding images

* You can add an image as one of your answers by correctly referencing as follows
	* Note: The image path should be relative to the file location or absolute
	* The file will name will not change on upload. 
		* In this case => "composite pattern.png"
		* This could lead to a conflict on Anki if files are named badly

* Check out the examples folder for a sample

```org
* What does the UML diagram for the compsite pattern look like?
** Image is displayed below
** [images_folder/composite pattern.png]
```

## Supported parameters

1. Each line must start with a hashtag
```org 
# type=Basic
# type = Basic
```

* Currently supported parameters are questions type

### File type => ```fileType```
    * Org or txt files will default to type basic.
    * If you want to use a topics layout this must be specified at the top of the file.

```org
# Comment line
# fileType=topics

* Topics 1
** Questions 1
*** Answer 1
```

### Anki Note type => ```type```
    * Used to set the type of the Anki note.
    * Default value is Basic
    * This is case sensitive and can be used to set any card type

```org
# type=Basic
# type=Basic (and reversed card)
```

### HTML list types => ```list``

    * Answers on cards are displayed as list
    * By default this will use an unordered

#### Unordered list (Default)
```org
# list=ul
# list=unordered
```

#### Ordered list 
```org
# list=ol
# list=ordered
```

#### No list 
```org
# list=false
```

## HTML code and LaTeX

* By default both HTML and Latex should be supported as they are in Anki

### HTML

* HTML formatting will be displayed as expected in Anki 
    * An example is show below

```org
* Question
** <b>Bold answer</b>
```

### LaTeX

* The best source on how to use LaTeX is the official documentation.
    * [Anki Documentation on Latex use](https://apps.ankiweb.net/docs/manual.html#latex-support)
* LaTeX added in any of the below formats will be rendered by Anki

Anki supports 3 different types of LaTeX formatting

* General LaTeX

```latex
[latex]...User specific latex..[/latex]
```

* Math Latex

```latex
[latex]\begin{math}...user specific latex...\end{math}[/latex]
```

This is shortened as follows

```org
[$]...[/$]
```

* DisplayMath LaTeX

```latex
[latex]\begin{math}...user specific latex...\end{math}[/latex]
```

This is shortened as follows

```org
[$$]...user specific latex...[/$$]
```

### Parameter inheritance

* Questions and decks will inhert parameters from parent Decks
* Parameters inhereted will not override existing parameters.
