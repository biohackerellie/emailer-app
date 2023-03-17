import os.path
import pickle
import google.auth.credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

#Define credential token
token = 'token.pickle'


#Checks for token, if none yet, pull credentials from secret.json file
creds = None
if os.path.exists('token.pickle'):
  with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.send'])
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)