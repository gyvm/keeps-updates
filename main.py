from __future__ import print_function
from os.path import os, join, dirname
import datetime

from flask import render_template, Flask
from dotenv import load_dotenv
import gkeepapi

app = Flask(__name__)


@app.route("/")
def index():
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    keep = gkeepapi.Keep()
    success = login(keep)
    if not success:
        return render_template('error.html', msg="Login failure", date=now)

    org_notes = keep.all()
    notes = get_note_title(org_notes)

    return render_template('index.html', notes=notes, date=now)


def get_note_title(org_notes):
    notes = []

    for org_note in org_notes:
        note = org_note
        print(org_note)
        if note.title == "":
            note.title = note.text.replace(' ', '')[0:99]

        notes.append(note)

    return notes


def login(keep):
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    success = False
    try:
        keep.login(username, password)
        success = True
    finally:
        return success


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",
            port=int(os.environ.get('PORT', 8080)))
