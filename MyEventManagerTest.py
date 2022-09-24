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

    # Add more test cases here

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

    #This test tests the create task function.

    def test_create_task(self):
        api = Mock()
        id = Entry(text = "test1111")
        name = Entry(text = "testnameee")
        loc = Entry(text="Online")
        att = Entry(text = "thisisanemail@gmail.com")
        start = DateEntry(date = "2022-09-25")
        end = DateEntry(date = "2022-09-26")

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
        test = MyEventManager.create_task(api, id, name, loc,att,start, end)
        self.assertEqual(
            api.test.return_value.list.return_value.execute.return_value.get.call_count, 0)

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


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()