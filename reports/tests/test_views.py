import logging
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)

class ReportsPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('reports/')
        self.assertTemplateUsed(response, 'reports/home.html')