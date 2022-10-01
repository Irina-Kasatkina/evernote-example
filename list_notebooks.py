import os

from dotenv import load_dotenv
from evernote.api.client import EvernoteClient

    
def main():
    load_dotenv() 
    is_sandbox = (os.environ['SANDBOX'] != 'False')
    if is_sandbox:
        evernote_personal_token = os.environ['EVERNOTE_SANDBOX_PERSONAL_TOKEN']
    else:
        evernote_personal_token = os.environ['EVERNOTE_PRODUCTION_PERSONAL_TOKEN']

    client = EvernoteClient(
        token=evernote_personal_token,
        sandbox=is_sandbox
    )
    note_store = client.get_note_store()

    notebooks = note_store.listNotebooks()
    for notebook in notebooks:
        print(f'{notebook.guid} - {notebook.name}')


if __name__ == '__main__':
    main()
