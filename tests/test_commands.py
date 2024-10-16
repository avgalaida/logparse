from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, MagicMock
from logs_app.models import LogEntry
from tests.factories import LogEntryFactory
import orjson
from django.utils import timezone


class ParseLogCommandTest(TestCase):
    @patch('requests.Session.get')
    def test_parse_log_command(self, mock_get):
        log_entry = LogEntryFactory.build()

        if timezone.is_naive(log_entry.timestamp):
            log_entry.timestamp = timezone.make_aware(log_entry.timestamp, timezone=timezone.utc)

        log_entry.timestamp = log_entry.timestamp.replace(microsecond=0)

        log_line = orjson.dumps({
            'time': log_entry.timestamp.strftime('%d/%b/%Y:%H:%M:%S %z'),
            'remote_ip': log_entry.ip_address,
            'request': f"{log_entry.http_method} {log_entry.uri} HTTP/1.1",
            'response': str(log_entry.response_code),
            'bytes': str(log_entry.response_size),
        }).decode('utf-8') + '\n'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content = MagicMock(return_value=[log_line.encode('utf-8')])
        mock_get.return_value = mock_response

        call_command('parse_log', 'https://drive.google.com/file/d/12345/view?usp=sharing')

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        entry_timestamp = entry.timestamp.replace(microsecond=0)

        self.assertEqual(entry_timestamp, log_entry.timestamp)
        self.assertEqual(entry.ip_address, log_entry.ip_address)
        self.assertEqual(entry.http_method, log_entry.http_method)
        self.assertEqual(entry.uri, log_entry.uri)
        self.assertEqual(entry.response_code, log_entry.response_code)
        self.assertEqual(entry.response_size, log_entry.response_size)
