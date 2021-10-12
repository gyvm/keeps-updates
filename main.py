from os.path import os, join, dirname
import datetime
import re

from flask import render_template, Flask
from dotenv import load_dotenv
import gkeepapi

from bs4 import BeautifulSoup
import concurrent.futures
import requests

bookmark_pages_dict = {}

app = Flask(__name__)


@app.route("/")
def index():
    now = datetime.datetime.utcnow()
    a_week_before = now + datetime.timedelta(days=-7)

    keep = gkeepapi.Keep()
    success = login(keep)
    if not success:
        return render_template('error.html', date=now)

    notes = keep.find(
        func=lambda note: note.timestamps.updated > a_week_before)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        [executor.submit(is_bookmark, note)
         for note in notes]

    return render_template('index.html', bookmark_pages_dict=bookmark_pages_dict, date=now)


def is_bookmark(note):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = re.findall(pattern, note.text)

    if len(url) > 0:
        if url[0] != "":
            site_title = get_site_title(url[0])
            if site_title != "":
                bookmark_pages_dict[url[0]] = site_title
            else:
                bookmark_pages_dict[url[0]] = url[0]


def get_site_title(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    site_title = soup.find("title").text

    return site_title


def login(keep):
    success = False

    try:
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")

        keep.login(username, password)
        success = True
    finally:
        return success


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",
            port=int(os.environ.get('PORT', 8080)))
