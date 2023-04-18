from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_num_unread_emails():
    """Returns the number of unread emails in the user's Gmail account."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'D:\OneDrive\Desktop\Jarvis\misc\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        num_unread = len(results.get('messages', []))
        return num_unread

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_subject_lines_unread_emails():
    """Returns a list of the subject lines of unread emails in the user's Gmail account."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'D:\OneDrive\Desktop\Jarvis\misc\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        if not messages:
            return None
        else:
            subject_lines = []
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                headers = msg['payload']['headers']
                subject = ''
                for header in headers:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                subject_lines.append(subject)
            return subject_lines

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

