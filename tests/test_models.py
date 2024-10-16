from django.test import TestCase
from logs_app.models import LogEntry
from tests.factories import LogEntryFactory


class LogEntryModelTest(TestCase):
    def test_create_log_entry(self):
        entry = LogEntryFactory()
        self.assertIsInstance(entry, LogEntry)
        self.assertIsNotNone(entry.ip_address)
        self.assertIsNotNone(entry.timestamp)
        self.assertIsNotNone(entry.http_method)
        self.assertIsNotNone(entry.uri)
        self.assertIsNotNone(entry.response_code)
        self.assertIsNotNone(entry.response_size)

    def test_str_method(self):
        entry = LogEntryFactory(ip_address='127.0.0.1', uri='/test/')
        self.assertEqual(str(entry), '127.0.0.1 - /test/')
