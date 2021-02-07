import time, os, io, re, json, logging, pickle
from seleniumwire import webdriver
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from urllib.request import urlretrieve
from google.cloud import vision
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/calendar"]
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=SCOPES)
if not os.path.exists("token.pkl"):
    credentials_OAuth = flow.run_console()
    pickle.dump(credentials_OAuth, open("token.pkl", "wb"))
else:
    credentials_OAuth = pickle.load(open("token.pkl", "rb"))

service = build('calendar', 'v3', credentials=credentials_OAuth)

calender_request = {
    "start": {
        "dateTime": ("2021-01-18T23:00:00" + "+10:00")
    },
    "end": {
        "dateTime": ("2021-01-18T23:00:00" + "+10:00")
    },
    "colorId": 11,
    "summary": "Work"
}
service.events().insert(calendarId="newmanbraydan@gmail.com", body=calender_request).execute()