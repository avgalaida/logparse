from django.urls import reverse
from rest_framework.test import APITestCase
from tests.factories import LogEntryFactory


class LogEntryAPITest(APITestCase):
    def setUp(self):
        self.entry1 = LogEntryFactory.create()
        self.entry2 = LogEntryFactory.create()

    def test_list_log_entries(self):
        url = reverse('logentry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_ip_address(self):
        url = reverse('logentry-list')
        response = self.client.get(url, {'ip_address': self.entry1.ip_address})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['ip_address'], self.entry1.ip_address)

    def test_search_by_uri(self):
        url = reverse('logentry-list')
        search_term = self.entry2.uri.split('/')[-1]
        response = self.client.get(url, {'search': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(entry['uri'] == self.entry2.uri for entry in response.data['results']))

    def test_pagination(self):
        LogEntryFactory.create_batch(20)
        url = reverse('logentry-list')
        response = self.client.get(url, {'limit': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
