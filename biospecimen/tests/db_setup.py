import logging
import sqlite3

from django.test import TestCase

logging.basicConfig(level=logging.CRITICAL)

class DatabaseSetup(TestCase):
    fixtures = ['initialdata']

    def setUp(self):
        self.client.login(username='testuser',password='secret')

