import json

import requests
from django.test import TestCase, Client


HTTP_HOST = 'http://localhost:8000/'

class VisitedLinksTest(TestCase):
    def empty_links(self):
        """Проверка пустого масссива ссылок"""
        data = {
            "links": [],
        }
        response = requests.post(HTTP_HOST + 'visited_links', json=data)
        self.assertEqual(response.status_code, 400)

    def incorrect_links(self):
        """Проверка некорректных ссылок"""
        data = {
            "links": [
                "abracadabra",
                "https:/abracadabra.ru"
            ]
        }
        response = requests.post(HTTP_HOST + 'visited_links', json=data)
        self.assertEqual(response.status_code, 409)

    def correct_links(self):
        """Проверка корректных ссылок"""
        data = {
            "links": [
                "https://vk.com",
                "https://vk2.com"
            ]
        }
        response = requests.post(HTTP_HOST + 'visited_links', json=data)
        self.assertEqual(response.status_code, 200)

class VisitedDomainsTest(TestCase):
    def incorrect_times(self):
        """Проверяет, что начало и конец - числа"""
        from_time = 'qqqq'
        to_time = 'qqqq'
        response = requests.get(HTTP_HOST + 'visited_domains' + '?from=' + from_time + '&to=' + to_time)
        self.assertEqual(response.status_code, 400)

    def from_more_to_times(self):
        """Проверяем, что начало меньше конца"""
        from_time = 1574677399
        to_time = from_time - 1
        response = requests.get(HTTP_HOST + 'visited_domains' + '?from=' + str(from_time) + '&to=' + str(to_time))
        self.assertEqual(response.status_code, 400)

    def correct_times(self):
        """Корректные данные"""
        from_time = 1571677399
        to_time = from_time + 3000000
        response = requests.get(HTTP_HOST + 'visited_domains' + '?from=' + str(from_time) + '&to=' + str(to_time))
        self.assertEqual(response.status_code, 200)
