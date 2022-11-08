import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'config/credentials.json'


def get_creds():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def update_schedule(creds):
    with open('schedule.json', mode='r') as file:
        unorderd_data = json.load(file)

    try:
        service = build('calendar', 'v3', credentials=creds)
        old_events = service.events().list(
            calendarId='11736a3d9cda7935cf0c1b9e18b6ef6c6cb34c01fa1b49f6bd0f2f7bb1dabe1a@group.calendar.google.com',
        ).execute()

        for item in old_events['items']:
            service.events().delete(
                calendarId='11736a3d9cda7935cf0c1b9e18b6ef6c6cb34c01fa1b49f6bd0f2f7bb1dabe1a@group.calendar.google.com',
                eventId=item['id']
            ).execute()

        for event_data in unorderd_data:
            if event_data['instructor'] is None:
                event_data['instructor'] = " "
            description = event_data['instructor'] + " " + event_data['remarks']
            datetime_start = event_data['date'] + 'T' + event_data['start']
            datetime_end = event_data['date'] + 'T' + event_data['end']
            event = {
                'summary': event_data['title'],
                'location': event_data['room'],
                'description': description,
                'start': {
                    'dateTime': datetime_start,
                    'timeZone': 'Europe/Zurich'
                },
                'end': {
                    'dateTime': datetime_end,
                    'timeZone': 'Europe/Zurich'
                }
            }

            service.events().insert(
                calendarId='11736a3d9cda7935cf0c1b9e18b6ef6c6cb34c01fa1b49f6bd0f2f7bb1dabe1a@group.calendar.google.com',
                body=event
            ).execute()

    except HttpError as error:
        print("something went wrong: ", error)
