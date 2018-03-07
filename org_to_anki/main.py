#!/usr/bin/env python3
# Script to parse differnet formated org files and upload them to Anki
import sys

from .org_parser import parseData
from .ankiConnectWrapper import AnkiConnector 
from . import config


def parse_and_upload_org_file(filePath=None):

	if filePath == None:
		firstArg = sys.argv[1:2]
		if len(firstArg) < 1:
			print("File was not given. Will upload default file.")
			filePath = config.quickNotesOrgPath
		else:
			filePath = filePath[0]

	if "~" in filePath:
		filePath = filePath.replace("~", config.homePath)

	print("file is ", filePath)
	_parse_and_upload(filePath)


def _parse_and_upload(filePath):

	questions = parseData.parse(filePath)
	connector = AnkiConnector.AnkiConnector()
	connector.uploadNewQuestions(questions)


if __name__ == "__main__":
	parse_and_upload_org_file()
