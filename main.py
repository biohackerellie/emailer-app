import datetime
import pytz
import os.path
import pickle
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import Credentials as OAuth2Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import googleapiclient.discovery_cache
from google_auth_oauthlib.flow import InstalledAppFlow
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import dateutil.parser
import os
from googleapiclient.discovery import build_from_document
import json
from google.auth.transport.requests import requests

DISCOVERY_DOC = 'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
GMAIL_DOC = 'https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest'

creds = None
if os.path.exists('token.pickle'):
  with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.send'])
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

CALENDAR_IDS = {
	"Graff": "gp0e5k830rv99igpjog6u9nq8iphetec@import.calendar.google.com",
	"LHS": "o1e6ujsge1jh88h6pnsqk34o48rnmv0c@import.calendar.google.com",
	"LMS": "4c4nlrab8h0b0pegriqncle0fsf5hisu@import.calendar.google.com",
	"South": "vu2b8tk83a69hlpl7eknu9blp123vaqn@import.calendar.google.com",
	"West": "pvr0fos16mog3d2jjb958t02rughplnd@import.calendar.google.com",
	"Stadium": "falu43smjvg8df797ndlbvunio6le757@import.calendar.google.com",
}


def get_calendar_events(service, calendar_id,):
	now = datetime.datetime.utcnow()

	timezone = pytz.timezone('US/Mountain')
	now = timezone.localize(now)

	start_of_week = (now - datetime.timedelta(days=now.weekday())).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-07:00' 
	end_of_week = (now + datetime.timedelta(days=7 - now.weekday())).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-07:00'

	events_result = service.events().list(calendarId=calendar_id, timeMin=start_of_week, timeMax=end_of_week, singleEvents=True, orderBy='startTime').execute()
	events = events_result.get('items', [])

	event_texts = []
	for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			start_datetime_utc = dateutil.parser.parse(start)
			mountain_tz = pytz.timezone('US/Mountain')
			start_datetime_mountain = start_datetime_utc.astimezone(mountain_tz)
			start_date = start_datetime_mountain.strftime('%A, %B %d, %Y')  # format start date as 'Weekday, Month day, Year'
			start_time = start_datetime_mountain.strftime('%I:%M %p')  # format start time as 'hh:mm AM/PM'
			event_text = event['summary'] + ' (' + start_date + ' at ' + start_time + ')\n\n'
			event_texts.append(event_text)
	return event_texts


def send_email(to, body, creds):

	gmail_service = build_from_document(json.loads(requests.get(GMAIL_DOC).text), credentials=creds)

	message = MIMEText(body)
	message['to'] = to
	message['subject'] = 'Weekly events'
	raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
	body = {'raw': raw}
	send_message = (gmail_service.users().messages().send(userId="me", body=body).execute())
	print(F'sent message to {to} Message Id: {send_message["id"]}')

def run_program():
	service = build_from_document(json.loads(requests.get(DISCOVERY_DOC).text), credentials=creds)
	to = to_entry.get()
	calendar_id_name = calendar_id_entry.get()
	calendar_id = CALENDAR_IDS.get(calendar_id_name)
	event_texts = get_calendar_events(service, calendar_id)
	message_body = 'Weekly events:\n\n'
	for event_texts in event_texts:
			message_body += event_texts
	send_email(to, message_body, creds)



root = tk.Tk()
root.title("Google Calendar Emailer")

to_label = tk.Label(root, text="To:")
to_label.grid(column=0, row=0, padx=5)
to_entry = tk.Entry(root, width=30)
to_entry.grid(column=1, row=0, padx=5, pady=5)

calendar_id_label = tk.Label(root, text="Calendar:")
calendar_id_label.grid(column=0, row=3, padx=5, pady=5)
calendar_id_entry = ttk.Combobox(root, width=27, state="readonly", values=list(CALENDAR_IDS.keys()))
calendar_id_entry.grid(column=1, row=3, padx=5, pady=5)


run_button = tk.Button(root, text="Run", command=run_program)
run_button.grid(column=1, row=4, padx=5, pady=5)




root.mainloop()


