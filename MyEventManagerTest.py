import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
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
        id = "Test12345"
        name = "test123"
        loc = "Online via Zoom"
        att = "yeeperngyew@gmail.com"
        start = "2022-09-24"
        end = "2022-09-25"

        event = {
        'summary': str(name),
        'location': str(loc),
        'id': str(id),
        'start': {
            'dateTime': str(start) + 'T00:00:00',
            'timeZone': 'GMT+8',
        },
        'end': {
            'dateTime': str(end) + 'T00:00:00',
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
        'sendUpdates': True,

    }
        test = MyEventManager.create_task(id, name, loc, att, start, end)
        self.assertEqual(
            api.test.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = api.test.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['id'], id)


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()