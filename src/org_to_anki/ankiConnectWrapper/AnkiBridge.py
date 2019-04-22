# Copyright (C) 2016 Alex Yatskov <alex@foosoft.net>
# Author: Alex Yatskov <alex@foosoft.net>
# This is a derivation of the work available here
# https://github.com/FooSoft/anki-connect/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

try:
    import anki
    import aqt
    from anki.sync import AnkiRequestsClient
except:
    anki = {}
    aqt = {}
    AnkiRequestsClient = {}

URL_TIMEOUT = 10

import base64
import hashlib

# This class imports anki and is used to interact with the database
class AnkiBridge:

    def __init__(self):

        self.x = "test"
        
    ### Core methods ###
    def addNote(self, note):
        ankiNote = self.createNote(note)

        audio = note.get('audio')
        if audio is not None and len(audio['fields']) > 0:
            try:
                data = self.download(audio['url'])
                skipHash = audio.get('skipHash')
                if skipHash is None:
                    skip = False
                else:
                    m = hashlib.md5()
                    m.update(data)
                    skip = skipHash == m.hexdigest()

                if not skip:
                    for field in audio['fields']:
                        if field in ankiNote:
                            ankiNote[field] += u'[sound:{}]'.format(audio['filename'])

                    self.media().writeData(audio['filename'], data)
            except Exception as e:
                errorMessage = str(e).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                for field in audio['fields']:
                    if field in ankiNote:
                        ankiNote[field] += errorMessage

        collection = self.collection()
        self.startEditing()
        collection.addNote(ankiNote)
        collection.autosave()
        self.stopEditing()

        return ankiNote.id

    def storeMediaFile(self, filename, data):
        self.deleteMediaFile(filename)
        self.media().writeData(filename, base64.b64decode(data))

    def createDeck(self, deck):
        try:
            self.startEditing()
            did = self.decks().id(deck)
        finally:
            self.stopEditing()

        return did

    def deckNames(self):
        return self.decks().allNames()

    def deleteMediaFile(self, filename):
        self.media().syncDelete(filename)

    ### Helper functions ###
    def startEditing(self):
        self.window().requireReset()


    def stopEditing(self):
        if self.collection() is not None:
            self.window().maybeReset()

    def decks(self):
        decks = self.collection().decks
        if decks is None:
            raise Exception('decks are not available')
        else:
            return decks

    def collection(self):
        collection = self.window().col
        if collection is None:
            raise Exception('collection is not available')
        else:
            return collection

    def window(self):
        return aqt.mw

    # Only works for python3
    def download(self, url):
        try:
            (code, contents) = self.download(url)
        except Exception as e:
            raise Exception('{} download failed with error {}'.format(url, str(e)))
        if code == 200:
            return contents
        else:
            raise Exception('{} download failed with return code {}'.format(url, code))

    def media(self):
        media = self.collection().media
        if media is None:
            raise Exception('media is not available')
        else:
            return media

    ### Note builder ###
    def createNote(self, note):
        collection = self.collection()

        model = collection.models.byName(note['modelName'])
        if model is None:
            raise Exception('model was not found: {}'.format(note['modelName']))

        deck = collection.decks.byName(note['deckName'])
        if deck is None:
            raise Exception('deck was not found: {}'.format(note['deckName']))

        ankiNote = anki.notes.Note(collection, model)
        ankiNote.model()['did'] = deck['id']
        ankiNote.tags = note['tags']

        for name, value in note['fields'].items():
            if name in ankiNote:
                ankiNote[name] = value

        allowDuplicate = False
        if 'options' in note:
          if 'allowDuplicate' in note['options']:
            allowDuplicate = note['options']['allowDuplicate']
            if type(allowDuplicate) is not bool:
              raise Exception('option parameter \'allowDuplicate\' must be boolean')

        duplicateOrEmpty = ankiNote.dupeOrEmpty()
        if duplicateOrEmpty == 1:
            raise Exception('cannot create note because it is empty')
        elif duplicateOrEmpty == 2:
          if not allowDuplicate:
            raise Exception('cannot create note because it is a duplicate')
          else:
            return ankiNote
        elif duplicateOrEmpty == False:
            return ankiNote
        else:
            raise Exception('cannot create note for unknown reason')