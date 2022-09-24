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
import calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
from time import strftime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


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


def get_events(api, starting_time, ending_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax = ending_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def openForm(tk):
    newWind = Toplevel(tk)
    newWind.title("Create Event")
    l1 = Label(newWind ,text = "Event ID").grid(row = 0,column = 0)
    l2 = Label(newWind ,text = "Event Name").grid(row = 1,column = 0)
    l3 = Label(newWind ,text = "Event Location").grid(row = 2,column = 0)
    l4 = Label(newWind ,text = "Event Attendees email").grid(row = 3,column = 0)
    l5 = Label(newWind ,text = "Start Date (yyyy-mm-dd)").grid(row = 4,column = 0)
    l6 = Label(newWind ,text = "End Date (yyyy-mm-dd)").grid(row = 5,column = 0)

    maxdate1 = date(2050,12,31)

    id = Entry(newWind)
    id.grid(row = 0,column = 1)
    name = Entry(newWind)
    name.grid(row = 1,column = 1)
    loc = Entry(newWind)
    loc.grid(row = 2,column = 1)
    att = Entry(newWind)
    att.grid(row = 3,column = 1)
    start = DateEntry(newWind, date_pattern='yyyy-mm-dd', maxdate = maxdate1)
    start.grid(row = 4,column = 1)
    end = DateEntry(newWind, date_pattern='yyyy-mm-dd', maxdate = maxdate1)
    end.grid(row = 5,column = 1)
    
    submitbtn = ttk.Button(newWind, text="Submit", command= lambda: create_task(id, name, loc, att, start, end)).grid(row = 6,column = 1)
    

    

def create_task(id, name, loc, att, start, end):
    api = get_calendar_api()
    eID = id.get()
    eName = name.get()
    eLoc = loc.get()
    eAtt = att.get()
    eStart = start.get()
    eEnd = end.get()

    event = {
        'summary': str(eName),
        'location': str(eLoc),
        'id': str(eID),
        'start': {
            'dateTime': str(eStart) + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': str(eEnd) + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'attendees': [
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            ],
        },
    }
    counter = 0
    emails = eAtt.split(',')
    for i in emails:
        event['attendees'].append({'email':str(i)})
        counter = counter + 1
        if counter >= 20:
            break
    
    event = api.events().insert(calendarId='primary', body=event).execute()
    

def clock(timelabel):
    string = strftime('%H:%M:%S %p')
    timelabel.config(text = "Current Time: " + string, font='bold')
    timelabel.after(1000, lambda: clock(timelabel))

def updating_tasks(tk, temp, clicked):
    api = get_calendar_api()

    year = temp.get()
    month = clicked.get()
    last_day = calendar.monthrange(int(year), int(month))[1]
    start_date = date(int(year), int(month), 1)
    end_date = date(int(year), int(month), last_day)
    start_time = str(start_date) + "T00:00:00Z"
    end_time = str(end_date) + "T00:00:00Z"
    events = get_events(api, start_time, end_time, 100)
    for event in events:
        eventsummary = Label(tk, text = "EventID: " + event['id'] + " Event Date/Time: " + event['start'].get('dateTime', event['start'].get('date')) + " Event Name: " + event['summary'])
        eventsummary.pack(pady = 10, anchor = "w")

def create_ui():
    tk = Tk()

    tk.geometry("1000x1000")
    tk.title("MyEventManager")
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    maxdate1 = date(2050,12,31)
    cal = Calendar(tk, selectmode = 'day', year = currentYear, month = currentMonth, day = currentDay, maxdate = maxdate1)
    cal.pack(pady = 20, fill = "both", expand = True)

    timelbl = Label(tk)
    timelbl.pack(pady = 10, anchor='center')
    clock(timelbl)

    btn = Button(tk, text="Create Event", command = lambda: openForm(tk))
    btn.pack(pady = 10)

    btn = Button(tk, text="Refresh Page", command = lambda: force_refresh(tk))
    btn.pack(pady = 10, anchor = 'w')

    header = Label(tk, text = "Events: ", font='bold')
    header.pack(pady = 10, anchor = "w")

    options_month = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12"
    ]
    clicked = StringVar()
    clicked.set("1")
    month_lbl = Label(tk, text = "Select Month: ")
    month_lbl.pack(anchor= "w")
    menu_month = OptionMenu(tk, clicked, *options_month)
    menu_month.pack(anchor = "w")

    year_lbl = Label(tk, text = "Input Year: ")
    year_lbl.pack(anchor= "w")
    temp = Entry(tk)
    temp.insert(0, "2022")
    temp.pack(anchor="w")
    
    btn = Button(tk, text="Get Events", command = lambda: updating_tasks(tk, temp, clicked))
    btn.pack(pady = 10, anchor = 'w')
    
    tk.mainloop()

def force_refresh(tk):
    tk.destroy()
    create_ui()

def main():
    create_ui()
   


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()