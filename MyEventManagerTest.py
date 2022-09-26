from asyncio import events
import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
# Add other imports here if needed

class MyEventManagerTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # This test tests number of upcoming events.
    def test_get_events(self):
        num_events = 3
        start = "2020-08-03T00:00:00.000000Z"
        end = "2020-08-04T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_events(mock_api, start, end, num_events)
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    def test_open_form(self):
        tk = Tk()
        mock_api = Mock()

        window = MyEventManager.openForm(tk, mock_api)
        self.assertEqual(window, 'normal')

    #This test tests the create task function.
    def test_create_task(self):
        api = Mock()
        id = Entry(text = "test1111")
        name = Entry(text = "testnameee")
        loc = Entry(text="Online")
        att = Entry(text = "thisisanemail@gmail.com")
        start = DateEntry(date = "2022-09-25")
        end = DateEntry(date = "2022-09-26")
        tk = Tk()
        newWind = Toplevel(tk)

        event = {
        'summary': name.get(),
        'location': loc.get(),
        'id': id.get(),
        'start': {
            'dateTime': start.get() + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': end.get() + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'attendees': [ {'email': att.get()}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            ],
        },
    }
        test = MyEventManager.create_task(newWind, api, id, name, loc,att,start, end)
        self.assertEqual(test, 0)

        var = api.mock_calls[1].kwargs['body']['id']
        self.assertEqual(var, id.get())

        var = api.mock_calls[1].kwargs['body']['summary']
        self.assertEqual(var, name.get())

        var = api.mock_calls[1].kwargs['body']['location']
        self.assertEqual(var, loc.get())

        var = api.mock_calls[1].kwargs['body']['attendees']
        self.assertEqual(var, [{'email': att.get()}])

        var = api.mock_calls[1].kwargs['body']['start']
        self.assertEqual(var, {'dateTime': start.get() + 'T00:00:00', 'timeZone': 'GMT+8'})

        var = api.mock_calls[1].kwargs['body']['end']
        self.assertEqual(var, {'dateTime': end.get() + 'T00:00:00', 'timeZone': 'GMT+8'})

    def test_updating_tasks(self):
        archive = []
        tk = Tk()
        temp = Entry(tk)
        temp.insert(0, "2022")
        clicked = StringVar()
        clicked.set("1")
        mock_api = Mock()

        test = MyEventManager.updating_tasks(archive, tk, temp, clicked, mock_api)
        self.assertEqual(test, 0)

    def test_populate(self):
        archive = []
        tk = Tk()
        event = [{"kind": "calendar#event", "etag": "3327718294364000", "id": "testidimport", "status": "confirmed", "htmlLink": "https://www.google.com/calendar/event?eid=M2plcmlndjNhbHM0azdhOTE1ZjVoY3I3b2Ygd2h1bzAwMDRAc3R1ZGVudC5tb25hc2guZWR1", "created": "2022-09-25T15:54:29.000Z", "updated": "2022-09-25T15:05:47.182Z", "summary": "This is Imported", "location": "Online", "creator": {"email": "whuo0004@student.monash.edu"}, "organizer": {"email": "whuo0004@student.monash.edu"}, "start": {"dateTime": "2022-09-28T16:00:00+11:00", "timeZone": "Asia/Singapore"}, "end": {"dateTime": "2022-09-29T16:30:00+11:00", "timeZone": "Asia/Singapore"}, "iCalUID": "testidimport@google.com", "sequence": 0, "attendees": [{"email": "wencheng31502@gmail.com", "self": "True", "responseStatus": "accepted"}], "guestsCanInviteOthers": "False", "guestsCanSeeOtherGuests": "False", "reminders": {"useDefault": "True"}, "eventType": "default"}]
        mock_api = Mock()
        test = MyEventManager.populate(event, archive, tk, mock_api)
        self.assertEqual(test, 0)

    def test_task_details(self):
        button_dict = {}
        archive = [] 
        tk = Tk() 
        event = {
        'summary': "tester123",
        'location': "online via zoom",
        'id': "test1234",
        'start': {
            'dateTime': "2022-09-25" + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': "2022-09-26" + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'attendees': [ {'email': 'yeeperngyew@gmail.com'}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            ],
            },
        }
        string = "EventID: " + event['id'] + " Event Date/Time: " + event['start'].get('dateTime', event['start'].get('date')) + " Event Name: " + event['summary']
        mock_api = Mock()
        mock_api.events().insert(calendarId='primary', body = event).execute()
        test = MyEventManager.task_details(button_dict, archive, tk, event, string, mock_api)
        self.assertEqual(test, 'normal')

    def test_accept_invite(self):
        tk = Tk()
        detailWind = Toplevel(tk)
        i = 0
        id = "tester123"
        mock_api = Mock()
        mock_api.event['attendees'][i]['responseStatus'] = 'accepted'
        print(mock_api)
        print(mock_api.event['attendees'][i]['responseStatus'])
        test = MyEventManager.accept_invite(detailWind, id, i, mock_api)
        self.assert_called()

    def test_reject_invite(self):
        tk = Tk()
        detailWind = Toplevel(tk)
        i = 0
        id = "tester123"
        mock_api = Mock()
        mock_api.event['attendees'][i]['responseStatus'] = 'declined'
        print(mock_api)
        print(mock_api.event['attendees'][i]['responseStatus'])
        test = MyEventManager.accept_invite(detailWind, id, i, mock_api)
        self.assert_called()

    def test_delete_task(self):
        button_dict = {'EventID: test1234 Event Date/Time: 2022-09-25T00:00:00 Event Name: tester123': ttk.Button()}
        tk = Tk()
        detailWind = Toplevel(tk)
        archive = []
        dateTimeStart = "2022-09-25T00:00:00"
        dateTimeEnd = "2022-09-26T00:00:00"
        id = "tester123"
        event = {
        'summary': "tester123",
        'location': "online via zoom",
        'id': "test1234",
        'start': {
            'dateTime': "2022-09-25" + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': "2022-09-26" + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'attendees': [ {'email': 'yeeperngyew@gmail.com'}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            ],
            },
        }
        mock_api = Mock()
        string = "EventID: " + event['id'] + " Event Date/Time: " + event['start'].get('dateTime', event['start'].get('date')) + " Event Name: " + event['summary']
        test = MyEventManager.delete_task(button_dict, detailWind, archive, dateTimeStart, dateTimeEnd, id, string, mock_api)

        self.assertEqual(test, 0)

    def test_archive_wind(self):
        tk = Tk()
        archive = []
        mock_api = Mock()
        test = MyEventManager.view_archive(tk, archive, mock_api)
        self.assertEqual(test, 'normal')

    def test_restore_event(self):
        i = 0
        button_dict = {i: ttk.Button()}
        mock_api = Mock()
        event = {
            'summary': "tester123",
            'location': "online via zoom",
            'id': "test1234",
            'start': {
                'dateTime': "2022-09-25" + 'T00:00:00',
                'timeZone': 'GMT+8',
            },
            'end': {
                'dateTime': "2022-09-26" + 'T00:00:00',
                'timeZone': 'GMT+8',
            },
            'attendees': [{'email': 'yeeperngyew@gmail.com'}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                ],
            },
        }
        archive = [event]
        test = MyEventManager.restore_event(button_dict, mock_api, archive, i)
        self.assertEqual(test, 0)
    
    def test_search_form(self):
        tk = Tk()
        mock_api = Mock()
        test = MyEventManager.search_form(tk, mock_api)
        self.assertEqual(test, 'normal')

    def test_search_event(self):
        btn = ttk.Button()
        tk = Tk()
        searchWind = Toplevel(tk)
        mock_api = Mock()
        search_term = Entry(searchWind)
        search_term.insert(0, "tester")
        test = MyEventManager.search_event(btn, searchWind, mock_api, search_term)
        self.assertEqual(test, 0)

    def test_print_details(self):
        mock_api = Mock()
        tk = Tk()
        searchWind = Toplevel(tk)
        event = {
            'summary': "tester123",
            'location': "online via zoom",
            'id': "test1234",
            'start': {
                'dateTime': "2022-09-25" + 'T00:00:00',
                'timeZone': 'GMT+8',
            },
            'end': {
                'dateTime': "2022-09-26" + 'T00:00:00',
                'timeZone': 'GMT+8',
            },
            'attendees': [{'email': 'yeeperngyew@gmail.com'}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                ],
            },
        }
        btn_dict = {event['summary']: ttk.Button()}
        test = MyEventManager.print_details(btn_dict, mock_api, searchWind, event['id'])
        self.assertEqual(test, ["EventID: " + event['id'],"Event Name: " + event['summary'],"Event Location: " + event['location'], "Event Start Date/Time: " + event['start'].get('dateTime', event['start']), "Event End Date/Time: " + event['end'].get('dateTime', event['end']), "Event Attendees: " + str(event['attendees'])])
        
    def test_import_json(self):
        mock_api = Mock()
        test = MyEventManager.import_json(mock_api) 
        self.assertEqual(test, 0)

    def test_export_json(self):
        mock_api = Mock()
        test = MyEventManager.export_json(mock_api)
        self.assertEqual(test, 1)

    def test_create_ui(self):
        archive = []
        mock_api = Mock()
        test = MyEventManager.create_ui(archive, mock_api)
        self.assertEqual(test, 0)


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()