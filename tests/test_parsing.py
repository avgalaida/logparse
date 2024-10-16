from django.test import TestCase
from logs_app.management.commands.parse_log import Command


class ParsingFunctionTest(TestCase):
    def setUp(self):
        self.command = Command()

    def test_valid_log_line(self):
        line = ('{"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "request": "GET '
                '/downloads/product_1 HTTP/1.1", "response": "200", "bytes": "490"}')
        obj = self.command.parse_line(line)
        self.assertEqual(obj.ip_address, '93.180.71.3')
        self.assertEqual(obj.http_method, 'GET')
        self.assertEqual(obj.uri, '/downloads/product_1')
        self.assertEqual(obj.response_code, 200)
        self.assertEqual(obj.response_size, 490)
