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
        all_events = list()
        page_token = None
        while True:
            service = build('calendar', 'v3', credentials=creds)
            events = service.events().list(
                calendarId='be9434ea5b1ebfd65d13472b8500ea69363b126a2e8fbab440fd055e2ea4c89a@group.calendar.google.com',
                pageToken=page_token
            ).execute()
            for event in events['items']:
                all_events.append(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        for event in all_events:
            service.events().delete(
                calendarId='be9434ea5b1ebfd65d13472b8500ea69363b126a2e8fbab440fd055e2ea4c89a@group.calendar.google.com',
                eventId=event.get("id")
            ).execute()

        for event_data in unorderd_data:
            if event_data['instructor'] is None:
                event_data['instructor'] = " "
                print("no instructor")
            description = event_data['instructor'] + " " + event_data['remarks']
            datetime_start = event_data['date'] + 'T' + event_data['start'] + ':00+01:00'
            datetime_end = event_data['date'] + 'T' + event_data['end'] + ':00+01:00'
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
                calendarId='be9434ea5b1ebfd65d13472b8500ea69363b126a2e8fbab440fd055e2ea4c89a@group.calendar.google.com',
                body=event,
            ).execute()

    except HttpError as error:
        print("something went wrong: ", error)
