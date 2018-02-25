#!/usr/bin/env python3
# Script to parse differnet formated org files and upload them to Anki
import sys, os
from os.path import expanduser
from org_to_anki import parseData
from org_to_anki import ankiConnectBridge

def main():
	print("starting")

def parse_and_upload_org_file(filePath=None):

	if filePath == None:
		firstArg = sys.argv[1:2]
		if len(firstArg) < 1:
			print("File was not given. Will upload default file.")
			home = expanduser("~")
			filePath = home + "/orgNotes/quickNotes.org"
			# dir = os.path.dirname(__file__)
			# filePath = os.path.join(dir, '../orgNotes/quickNotes.org')
		else:
			filePath = filePath[0]
		
	questions = parseData.parse(filePath)
	
	connector = ankiConnectBridge.AnkiConnectBridge()
	connector.uploadNewQuestions(questions)

def test():
	print("starting")

if __name__ == "__main__":
	parse_and_upload_org_file("/Users/cokelly/Desktop/Personal_Dev/org_to_anki/orgNotes/quickNotes.org")
