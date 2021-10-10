from __future__ import print_function
from os.path import os, join, dirname
import datetime
import re

from flask import render_template, Flask
from dotenv import load_dotenv
import gkeepapi

bookmark_pages = []

app = Flask(__name__)


@app.route("/")
def index():
    keep = gkeepapi.Keep()
    success = login(keep)
    if not success:
        print("error")

    now = datetime.datetime.utcnow()
    a_week_before = now + datetime.timedelta(days=-7)

    notes = keep.find(
        func=lambda note: note.timestamps.updated > a_week_before)

    for note in notes:
        is_bookmark(note)

    print(bookmark_pages)
    return render_template('index.html', bookmark_pages=bookmark_pages, date=now)


def is_bookmark(note):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = re.findall(pattern, note.text)

    if len(url) > 0:
        if url[0] != "":
            bookmark_pages.append(url[0])


def list2link(list):
    str = ','.join(["<a href='search?q=" + x +
                   "'>" + x + "</a>" for x in list])
    return str


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
