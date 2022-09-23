# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from time import strftime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def openForm():
    newWind = Toplevel(tk)
    newWind.title("Create Event")
    newWind.geometry("500x500")

def clock():
    string = strftime('%H:%M:%S %p')
    timelbl.config(text = "Current Time: " + string, font='bold')
    timelbl.after(1000, clock)

tk = Tk()

tk.geometry("700x700")
tk.title("MyEventManager")

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
cal = Calendar(tk, selectmode = 'day', year = currentYear, month = currentMonth, day = currentDay)
cal.pack(pady = 20, fill = "both", expand = True)

api = get_calendar_api()
time_now = datetime.utcnow().isoformat() + 'Z'
events = get_upcoming_events(api, time_now, 100)

timelbl = Label(tk)
timelbl.pack(pady = 10, anchor='center')
clock()

btn = Button(tk, text="Create Event", command = openForm)
btn.pack(pady = 10)

header = Label(tk, text = "Events: ", font='bold')
header.pack(pady = 10, anchor = "w")
for event in events:
    eventsummary = Label(tk, text = event['start'].get('dateTime', event['start'].get('date')) + " " + event['summary'])
    eventsummary.pack(pady = 10, anchor = "w")

tk.mainloop()


def main():
    api = get_calendar_api()
    time_now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()