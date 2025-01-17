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
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tkinter import *
from tkinter import ttk, messagebox, filedialog
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


def openForm(tk, api):
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
    submitbtn = ttk.Button(newWind, text="Submit", command= lambda: create_task(newWind, api, id, name, loc,att,start, end)).grid(row = 6,column = 1)
    return newWind.state()
    

def create_task(newWind, api, id, name, loc,att,start, end):
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
    try:
        event = api.events().insert(calendarId='primary', body=event, sendUpdates = 'all').execute()
        newWind.destroy()
        return 0
    except Exception as e:
        messagebox.showinfo(title=None, message="Create Event Failed: " + str(e))
        return 1
    

def updating_tasks(archive, tk, temp, clicked, api):
    year = temp.get()
    month = clicked.get()
    last_day = calendar.monthrange(int(year), int(month))[1]
    start_date = date(int(year), int(month), 1)
    end_date = date(int(year), int(month), last_day)
    start_time = str(start_date) + "T00:00:00Z"
    end_time = str(end_date) + "T00:00:00Z"
    events = get_events(api, start_time, end_time, 100)
    populate(events, archive, tk, api)
    return 0

def populate(events, archive, tk, api):
    button_dict = {}
    option = []
    for event in events:
        option.append(["EventID: " + event['id'] + " Event Date/Time: " + event['start'].get('dateTime', event['start'].get('date')) + " Event Name: " + event['summary'], event]) 
    
    try:
        for i in option:
            string = i[0]
            event1 = i[1]
            def disp(x=event1):
                return task_details(button_dict, archive, tk, x, string, api)
            button_dict[string] = ttk.Button(tk, text=string, command=disp)
            button_dict[string].pack(anchor = 'w')
        return 0
    except Exception as e:
        messagebox.showinfo(title=None, message="An exception occured! " + str(e))
        return 1

def task_details(button_dict, archive, tk, event, string, api):
    detailWind = Toplevel(tk)
    detailWind.title("Details for Selected Task")
    detailWind.geometry("500x300")
    e1 = Label(detailWind, text = "EventID: " + event['id'])
    e2 = Label(detailWind, text = "Event Name: " + event['summary'])
    e3 = Label(detailWind, text = "Event Location: " + event['location'])
    e4 = Label(detailWind, text = "Event Start Date/Time: " + event['start'].get('dateTime', event['start']))
    e5 = Label(detailWind, text = "Event End Date/Time: " + event['end'].get('dateTime', event['end']))
    try:
        e6 = Label(detailWind, text = "Event Attendees: " + str(event['attendees']))
    except Exception as e:
        e6 = Label(detailWind, text="No valid attendees found")
        delbtn = ttk.Button(detailWind, text="Delete/Cancel Event", command=lambda: delete_task(button_dict, detailWind, archive, event['start'].get('dateTime'),event['end'].get('dateTime'), event['id'], string, api))
        delbtn.pack(anchor='center')
    e1.pack(anchor='w')
    e2.pack(anchor='w')
    e3.pack(anchor='w')
    e4.pack(anchor='w')
    e5.pack(anchor='w')
    e6.pack(anchor='w')
    cal = api.calendars().get(calendarId='primary').execute()
    for i in range(len(event['attendees'])):
        if event['attendees'][i]['email'] ==  cal['summary'] and event['attendees'][i]['responseStatus'] == 'needsAction':
            accept_btn = ttk.Button(detailWind, text= "Accept", command = lambda: accept_invite(detailWind, event['id'], i, api))
            reject_btn = ttk.Button(detailWind, text="Reject", command=lambda: reject_invite(detailWind, event['id'], i, api))
            accept_btn.pack(anchor='w')
            reject_btn.pack(anchor='w')
            break
    delbtn = ttk.Button(detailWind, text="Delete/Cancel Event", command=lambda: delete_task(button_dict, detailWind, archive, event['start'].get('dateTime'),event['end'].get('dateTime'), event['id'], string, api))
    delbtn.pack(anchor='w')
    return detailWind.state()

def accept_invite(detailWind, id, i, api):
    event = api.events().get(calendarId='primary', eventId=id).execute()
    event['attendees'][i]['responseStatus'] = 'accepted'
    api.events().update(calendarId='primary', eventId=id, body=event).execute()
    detailWind.destroy()
    return 0

def reject_invite(detailWind, id, i, api):
    event = api.events().get(calendarId='primary', eventId=id).execute()
    event['attendees'][i]['responseStatus'] = 'declined'
    api.events().update(calendarId='primary', eventId=id, body=event).execute()
    detailWind.destroy()
    return 0
    
def delete_task(button_dict, detailWind, archive, dateTimeStart, dateTimeEnd, id, string, api):
    tempS = dateTimeStart.split('T')[0].split('-')
    tempE = dateTimeEnd.split('T')[0].split('-')
    date_start = date(int(tempS[0]),int(tempS[1]), int(tempS[2]))
    date_end = date(int(tempE[0]), int(tempE[1]), int(tempE[2]))
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    date_now = date(currentYear, currentMonth, currentDay)
    
    if date_start >= date_now or date_end >= date_now:
        archive.append(api.events().get(calendarId='primary', eventId=id).execute())
        api.events().delete(calendarId='primary', eventId=id).execute()
        detailWind.destroy()
        button_dict[string].destroy()
        messagebox.showinfo(title=None, message="Event Cancelled Successfully, event added to archive")
        return 0
    else:
        api.events().delete(calendarId='primary', eventId=str(id)).execute()
        detailWind.destroy()
        button_dict[string].destroy()
        messagebox.showinfo(title=None, message="Event Deleted Successfully")
        return 0

def view_archive(tk, archive, api):
    archive_wind = Toplevel(tk)
    archive_wind.title("Archive")
    l1 = Label(archive_wind, text= "Cancelled Events:")
    l1.pack(anchor = 'center')
    button_dict = {}
    for i in range(len(archive)):
        for j in archive:
            button_dict[i] = ttk.Button(archive_wind, text= j['summary'], command= lambda: restore_event(button_dict, api, archive, i))
        button_dict[i].pack(anchor='center')
    l2 = Label(archive_wind, text= "Select to restore")
    l2.pack(anchor = 'center')
    return archive_wind.state()

def restore_event(button_dict, api, archive, i):
    start_date = archive[i]['start']['dateTime'].split("T")[0]
    end_date = archive[i]['end']['dateTime'].split("T")[0]
    event = {
        'summary': archive[i]['summary'],
        'location': archive[i]['location'],
        'id': archive[i]['id'] + "n",
        'start': {
            'dateTime': start_date + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': end_date + 'T00:00:00',
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
    try:
        event = api.events().insert(calendarId='primary', body=event, sendUpdates = 'all').execute()
        archive.remove(archive[i])
        button_dict[i].destroy()
        messagebox.showinfo(title=None, message="Restore Event Successful")
        return 0
    except Exception as e:
        messagebox.showinfo(title=None, message="Restore Event Failed: " + str(e))
        return 1

def search_form(tk, api):
    searchWind = Toplevel(tk)
    searchWind.title("Search Window")
    searchWind.geometry("800x500")

    l1 = Label(searchWind ,text = "Search by Event Name: ")
    search_term = Entry(searchWind)
    l1.pack(anchor = 'center')
    search_term.pack(anchor='center')
    btn = Button(searchWind, text="Search", command = lambda: search_event(btn, searchWind, api, search_term))
    btn.pack(anchor = 'center')
    return searchWind.state()

def search_event(btn, searchWind, api, search_term):
    Id_list = []
    btn_dict = {}
    term = search_term.get()
    list_events = api.events().list(calendarId='primary', q=str(term)).execute()
    for event in list_events['items']:
        Id_list.append(event['id'])
    
    for id in Id_list:
        event = api.events().get(calendarId='primary', eventId = id).execute()
        btn_dict[event['summary']] = ttk.Button(searchWind, text = event['summary'], command= lambda: print_details(api, searchWind, id))
        btn_dict[event['summary']].pack(anchor='center')
    btn.destroy()
    return 0

def print_details(api, searchWind, id):
    event = api.events().get(calendarId='primary', eventId=id).execute()
    e1 = Label(searchWind, text = "EventID: " + event['id'])
    e2 = Label(searchWind, text = "Event Name: " + event['summary'])
    e3 = Label(searchWind, text = "Event Location: " + event['location'])
    e4 = Label(searchWind, text = "Event Start Date/Time: " + event['start'].get('dateTime', event['start']))
    e5 = Label(searchWind, text = "Event End Date/Time: " + event['end'].get('dateTime', event['end']))
    try:
        e6 = Label(searchWind, text = "Event Attendees: " + str(event['attendees']))
    except Exception as e:
        e6 = Label(searchWind, text="No valid attendees found")
    e1.pack(anchor='w')
    e2.pack(anchor='w')
    e3.pack(anchor='w')
    e4.pack(anchor='w')
    e5.pack(anchor='w')
    e6.pack(anchor='w')
    return 0

def import_json(api):
    filename = filedialog.askopenfilename()
    file_ext = filename.split(".")[-1]
    if file_ext == "json":
        with open(filename.split("/")[-1], 'r') as openfile:
            json_object = json.load(openfile)
    else:
        messagebox.showinfo(title=None, message="Import Failed: Invalid File")
        return 1
    
    for i in json_object:
        start_date = i['start']['dateTime'].split("T")[0]
        end_date = i['end']['dateTime'].split("T")[0]
        event = {
        'summary': i['summary'],
        'location': i['location'],
        'id': i['id'] + "n",
        'start': {
            'dateTime': start_date + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': end_date + 'T00:00:00',
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
    try:
        event = api.events().insert(calendarId='primary', body=event, sendUpdates = 'all').execute()
        messagebox.showinfo(title=None, message="Imported Successfully")
        return 0
    except Exception as e:
        messagebox.showinfo(title=None, message="Import Failed: " + str(e))
        return 1
        

def export_json(api):
    try:
        event_list = api.events().list(calendarId='primary').execute()
        with open("export.json", "w") as outfile:
            json.dump(event_list, outfile)
    
        messagebox.showinfo(title=None, message="Exported Successfully")
        return 0
    except Exception as e:
        messagebox.showinfo(title=None, message="Export Failed: " + str(e))
        return 1
    

def create_ui(archive, api):
    tk = Tk()
    tk.geometry("850x1000")
    tk.title("MyEventManager")
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    maxdate1 = date(2050,12,31)
    cal = Calendar(tk, selectmode = 'day', year = currentYear, month = currentMonth, day = currentDay, maxdate = maxdate1)
    cal.pack(pady = 20, fill = "both", expand = True)

    btn = Button(tk, text="Create Event", command = lambda: openForm(tk, api))
    btn.pack(pady = 10)

    btn = Button(tk, text="View Event Archive", command = lambda: view_archive(tk, archive, api))
    btn.pack(pady = 10, anchor = 'center')

    btn = Button(tk, text="Import JSON", command = lambda: import_json(api))
    btn.pack(pady = 10, anchor = 'center')

    btn = Button(tk, text="Export JSON", command = lambda: export_json(api))
    btn.pack(pady = 10, anchor = 'center')

    btn = Button(tk, text="Clear Events", command = lambda: force_refresh(tk, archive, api))
    btn.pack(pady = 10, anchor = 'w')

    header = Label(tk, text = "Events: ", font='bold')
    header.pack(pady = 10, anchor = "w")

    btn = Button(tk, text="Search Events", command = lambda: search_form(tk, api))
    btn.pack(pady = 10, anchor = 'w')

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
    
    btn = Button(tk, text="Get Events", command = lambda: updating_tasks(archive, tk, temp, clicked, api))
    btn.pack(pady = 10, anchor = 'w')
    
    tk.mainloop()
    return 0

def force_refresh(tk, archive, api):
    tk.destroy()
    create_ui(archive, api)

def main():
    archive = []
    api = get_calendar_api()
    create_ui(archive, api)
   


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()