from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def get_e_mail():
    fromm = input("Adja meg az email feladóját! ")
    too = input("Adja meg az email címzettjét! ")
    subj = input("Adja meg az email tárgyát! ")
    cont = input("Adja meg az email tartalmát! ")
    data = [fromm, too, subj, cont]
    return data


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def send_message(service):
    message = EmailMessage()
    items = get_e_mail()

    message.set_content(items[3])

    message['To'] = items[1]
    message['From'] = items[0]
    message['Subject'] = items[2]

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')


def main():
    print("Ez a program elküld egy emailt a felhasználó által megadott adatok alapján.")
    service = get_service()
    send_message(service)


main()
