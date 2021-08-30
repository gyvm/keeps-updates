from __future__ import print_function
import os.path
import datetime

# for get_credentials()
from googleapiclient.discovery import build
import google.auth

# for get_oauth_credentials()
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import render_template, Flask

SCOPES = ['https://www.googleapis.com/auth/keep']
# SCOPES = ['https://www.googleapis.com/auth/keep.readonly']

app = Flask(__name__)


@app.route("/keeps-updates")
def index():
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    creds = get_credentials()
    # creds = get_oauth_credentials()

    service = build('keep', 'v1', credentials=creds)
    notes_result = service.notes().list(
        pageSize=10).execute()
    print(notes_result)

    notes = {'notes': str(notes_result)}

    return render_template('index.html', notes=notes, date=now)


def get_credentials():
    creds = google.auth.load_credentials_from_file(
        './credentials.json', SCOPES)[0]

    return creds


def get_oauth_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",
            port=int(os.environ.get('PORT', 8080)))
