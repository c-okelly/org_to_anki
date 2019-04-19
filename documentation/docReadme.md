
# Word or LibreOffice files

1. [File syntax](#File-syntax) 
2. [Saving files](#Saving-Word-or-LibreOffice-files) 
3. [Code Highlighting](#code-highlighting)
4. [Supported parameters](https://github.com/c-okelly/org_to_anki/blob/master/documentation/orgReadme.md#Supported-parameters)
5. [HTML code and LaTeX](https://github.com/c-okelly/org_to_anki/blob/master/documentation/orgReadme.md#html-code-and-latex)

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


## Code Highlighting

This parser support code highlighting using the Pygments library.

[Supported Languages](http://pygments.org/languages/)

Example syntax below:

```org
	* Give me some basic python
	```python3
	print("Hello world!")

	if (True):
		print("Even indents!")
	```
```


This would produce the following card:

![code file](../gifs/code_card.png)
