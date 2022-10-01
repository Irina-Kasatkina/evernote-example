#!/usr/bin/env python 
import argparse
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore

    
def get_notebook_list(note_store, notebook_guid, number=10, offset=0):
    _filter = NoteStore.NoteFilter(notebookGuid=notebook_guid)
    result_spec = NoteStore.NotesMetadataResultSpec(
        includeTitle=True,
        includeContentLength=True,
        includeCreated=True,
        includeUpdated=True,
        includeDeleted=False,
        includeUpdateSequenceNum=True,
        includeNotebookGuid=True,
        includeTagGuids=True,
        includeAttributes=True,
        includeLargestResourceMime=True,
        includeLargestResourceSize=True,
    )

    # this determines which info you'll get for each note
    return note_store.findNotesMetadata(_filter, offset, number, result_spec);


def main():
    load_dotenv() 
    is_sandbox = (os.environ['SANDBOX'] != 'False')
    if is_sandbox:
        evernote_personal_token = os.environ['EVERNOTE_SANDBOX_PERSONAL_TOKEN']
    else:
        evernote_personal_token = os.environ['EVERNOTE_PRODUCTION_PERSONAL_TOKEN']
    notebook_guid = os.environ['INBOX_NOTEBOOK_GUID']

    parser = argparse.ArgumentParser(description=u'Dumps notes from Evernote inbox to console')
    parser.add_argument('number', nargs='?', type=int, default=10, help='number of records to dump')
    parser.add_argument('guid', nargs='?', type=str, default=notebook_guid, help='notebook GUID')
    args = parser.parse_args()
    notebook_guid = args.guid

    client = EvernoteClient(
        token=evernote_personal_token,
        sandbox=is_sandbox
    )

    note_store = client.get_note_store()

    notes = get_notebook_list(note_store, notebook_guid, args.number).notes
    
    for counter, note in enumerate(notes, start=1):
        print(f'\n--------- {counter} ---------')
        print(f'Note GUID: {note.guid}')
        print(f'Note title: {note.title}')
        content = note_store.getNoteContent(note.guid)
        soup = BeautifulSoup(content, features='xml')
        for div_tag in soup.find_all('div'):
            print(div_tag.text)


if __name__ == '__main__':
    main()
