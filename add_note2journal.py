#!/usr/bin/env python 
from datetime import date, datetime, timedelta
import argparse
import json
import os

from dotenv import load_dotenv
from evernote.api.client import EvernoteClient


WEEK_DAYS = {
    1: u'понедельник',
    2: u'вторник',
    3: u'среда',
    4: u'четверг',
    5: u'пятница',
    6: u'суббота',
    7: u'воскресенье',
}


def is_valid_date(text):
    text = text.strip()
    if text.startswith('-') or text.startswith('+') or text.isdigit():
        return date.today() + timedelta(days=int(text))
    try:

        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(text)
        raise argparse.ArgumentTypeError(msg)


def main():
    load_dotenv() 
    is_sandbox = (os.environ['SANDBOX'] != 'False')
    if is_sandbox:
        evernote_personal_token = os.environ['EVERNOTE_SANDBOX_PERSONAL_TOKEN']
    else:
        evernote_personal_token = os.environ['EVERNOTE_PRODUCTION_PERSONAL_TOKEN']
    journal_template_note_guid = os.environ['JOURNAL_TEMPLATE_NOTE_GUID']
    journal_notebook_guid = os.environ['JOURNAL_NOTEBOOK_GUID']

    parser = argparse.ArgumentParser(description=u'Adds note to notebook "Дневник", uses template note')
    parser.add_argument('date',
                        nargs='?',
                        type=is_valid_date,
                        help='date in format "YYYY-MM-DD"')
    args = parser.parse_args()

    client = EvernoteClient(
        token=evernote_personal_token,
        sandbox=is_sandbox
    )
    note_store = client.get_note_store()

    day = args.date or date.today()
    context = {
        'date': day.isoformat(),
        'dow': WEEK_DAYS[day.isoweekday()],
    }
    print('Title Context is:')
    print(json.dumps(context, ensure_ascii=False, indent=4))

    new_note = note_store.copyNote(journal_template_note_guid, journal_notebook_guid)
    utitle_without_comment = new_note.title.split('#', 1)[0]
    utitle = utitle_without_comment.strip().format(**context)
    new_note.title = utitle
    note_store.updateNote(new_note)
    
    print(f'Note created: {utitle}')
    print('Done')


if __name__ == '__main__':
    main()
