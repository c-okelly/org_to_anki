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
    from aqt.utils import showInfo
except:
    anki = {}
    aqt = {}
    AnkiRequestsClient = {}

URL_TIMEOUT = 10

import base64
import hashlib
import os
import unicodedata

# This class imports anki and is used to interact with the database
class AnkiBridge:

    def __init__(self):

        self.x = "test"
        
    ### Core methods ###
    def addNote(self, note):
        ankiNote = self.createNote(note)
        if ankiNote == None:
            return

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
        try:
            self.media().syncDelete(filename)
        except AttributeError:
            self.media().trash_files([filename])

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
            showInfo("Warning. The following note could note be created:\nPossible reasons include strangely configured local note models\n{}".format(note))
        elif duplicateOrEmpty == 2:
          if not allowDuplicate:
              return None 
            # showInfo("Warning. The following note could note be created because it is a duplicate:\n{}".format(note))
          else:
            return ankiNote
        elif duplicateOrEmpty == False:
            return ankiNote
        else:
            showInfo("Warning. The following note could note be created. Reason unknown:\n{}".format(note))

    # Check if models are present 
    def modelNames(self):
        return self.collection().models.allNames()

    def createModel(self, modelName, inOrderFields, cardTemplates, css = None):
        # https://github.com/dae/anki/blob/b06b70f7214fb1f2ce33ba06d2b095384b81f874/anki/stdmodels.py
        if (len(inOrderFields) == 0):
            raise Exception('Must provide at least one field for inOrderFields')
        if (len(cardTemplates) == 0):
            raise Exception('Must provide at least one card for cardTemplates')
        if (modelName in self.collection().models.allNames()):
            raise Exception('Model name already exists')

        collection = self.collection()
        mm = collection.models

        # Generate new Note
        m = mm.new(modelName)

        # Create fields and add them to Note
        for field in inOrderFields:
            fm = mm.newField(field)
            mm.addField(m, fm)

        # Add shared css to model if exists. Use default otherwise
        if (css is not None):
            m['css'] = css

        # Generate new card template(s)
        cardCount = 1
        for card in cardTemplates:
            t = mm.newTemplate('Card ' + str(cardCount))
            cardCount += 1
            t['qfmt'] = card['Front']
            t['afmt'] = card['Back']
            mm.addTemplate(m, t)

        mm.add(m)
        return m

    ### Methods used by remote-decks only ###
    def deleteNotes(self, noteId):
        self.startEditing()
        try:
            aqt.mw.col.remNotes([noteId])
        finally:
            self.stopEditing()

    def updateNoteFields(self, note):

        # showInfo("{}".format(note['id']))

        ankiNote = aqt.mw.col.getNote(note['id'])
        # showInfo("{}".format(ankiNote))
        if ankiNote is None:
            raise Exception('note was not found: {}'.format(note['id']))

        for name, value in note['fields'].items():
            if name in ankiNote:
                ankiNote[name] = value

        ankiNote.flush()


    # Core current method
    def getDeckNotes(self, deckName):

        cardIds = self._getAnkiCardIdsForDeck(deckName)
        # showInfo("{}".format(cardIds))

        cards = self._getCardsFromIds(cardIds)

        return cards

    def _getAnkiCardIdsForDeck(self, deckName):


        # TODO should check if deck name is in the correct format

        # Make query to Anki
        queryTemplate = "deck:\"{}\""

        query = queryTemplate.format(deckName)
        # showInfo("{}".format(query))

        ids = self.collection().findNotes(query)

        return ids


    def _getCardsFromIds(self, AnkiCardsIds):

        result = []
        for nid in AnkiCardsIds:
            # TODO possible error handling
            note = self.collection().getNote(nid)
            model = note.model()

            fields = {}
            for info in model['flds']:
                order = info['ord']
                name = info['name']
                fields[name] = {'value': note.fields[order], 'order': order}

            result.append({
                'noteId': note.id,
                'tags' : note.tags,
                'fields': fields,
                'modelName': model['name'],
                'cards': self.collection().db.list('select id from cards where nid = ? order by ord', note.id)
            })

        return result
    
    def checkForMediaFile(self, filename):
        filename = os.path.basename(filename)
        filename = unicodedata.normalize('NFC', filename)
        filename = self.media().stripIllegal(filename)

        path = os.path.join(self.media().dir(), filename)
        if os.path.exists(path):
            return True
        else:
            return False
