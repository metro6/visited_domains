import json

from django.test import TestCase, Client


class VisitedLinksTest(TestCase):
    def empty_links(self):
        c = Client()
        response = c.post('/visited_links', data={'links': ['']})
        self.assertEqual(response.status_code, 400)

    def incorrect_links(self):
        c = Client()
        response = c.post('/visited_links', data={'links': ['abracadabra', 'https:/abracadabra.ru']})
        self.assertEqual(response.status_code, 400)

    def correct_links(self):
        c = Client()
        response = c.post('/visited_links', data={'links': ["https://vk.com", 'https://vk2.com']})
        self.assertEqual(response.status_code, 200)

class VisitedDomains(TestCase):
    pass