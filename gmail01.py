from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_informations(i):
    fromm = input(f"\nSzeretnéd a(z) {i}. beérkező leveled feladóját megtekinteni? (Üss egy ENTER-t ha igen, ha nem, "
                  "akkor írd hogy 'nem') ")
    subject = input(f"Szeretnéd a(z) {i}. beérkező leveled tárgyát megtekinteni? (Üss egy ENTER-t ha igen, ha nem, "
                    "akkor írd hogy 'nem') ")
    date = input(f"Szeretnéd a(z) {i}. beérkező leveled dátumát megtekinteni? (Üss egy ENTER-t ha igen, ha nem, "
                 "akkor írd hogy 'nem') ")
    print("\n")
    data = [fromm, subject, date]
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


def get_messages(service):
    results = service.users().messages().list(userId='me').execute()
    msg_ids = []
    for msg in results['messages']:
        msg_ids.append(msg['id'])
    number = int(input("Add meg a megjelenítendő beérkezett emailek számát! "))
    i = 1
    for index in range(number):
        message = service.users().messages().get(userId='me',
                                                 id=msg_ids[index], format='metadata').execute()
        headers = message['payload']['headers']
        informations = get_informations(i)
        for header in headers:
            if header['name'] == 'From' and informations[0] == "":
                print(f'From: {header["value"]}')
            elif header['name'] == 'Subject' and informations[1] == "":
                print(f'Subject: {header["value"]}')
            elif header['name'] == 'Date' and informations[2] == "":
                print(f'\nDate: {header["value"]}')
        i += 1


def main():
    print("Ez a program kilistázza a felhasználó beérkezett emaileit.\n")
    service = get_service()
    get_messages(service)


main()
