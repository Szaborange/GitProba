from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_labels(r):
    labels = r.get('labels', [])
    if not labels:
        print('No labels found.')
        return
    print('Labels:')
    for label in labels:
        print(label['name'])


def get_service(c):
    service = build('gmail', 'v1', credentials=c)
    results = service.users().labels().list(userId='me').execute()
    get_labels(results)


def main():
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

    get_service(creds)


main()
