from __future__ import print_function
from datetime import datetime, timedelta
import time
import pickle
import webbrowser
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import schedule
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
webbrowser.register('firefox',None, webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
##you must have plain text zoom links in your google event's description for this to work.
def controller():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow()
    then = now + timedelta(hours = 12)
    now = now.isoformat() + 'Z'
    then = then.isoformat() + 'Z'
    print('Getting classes for',now[:10])
    events_result = service.events().list(calendarId='eli.cox@frogslayer.com',timeMax = then,timeMin=now,maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        if event['summary'][:4] == 'CSCE' or event['summary'][:4] == 'MATH': ##change this line to filter your classes
                event_time = datetime.strptime(event['start'].get('dateTime')[:19], '%Y-%m-%dT%H:%M:%S').time()
                while True:
                    try:
                        now_time = datetime.now().time()
                        if now_time > event_time or now_time == event_time:
                            print(event['summary'],'has started.')
                            webbrowser.get('firefox').open(event['description'])
                            break
                        else:
                            time.sleep(60)
                    except KeyboardInterrupt:
                        print("Quitting...")
                        exit()
    if not events:
        print('No upcoming events found for',now[:10])

def main():
    print('ZOOM BOT. STARTING...')
    controller() #should only run if > 08:00
    schedule.every().day.at("08:00").do(controller)
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            print("Quitting...")
            exit()

if __name__ == '__main__':
    main()