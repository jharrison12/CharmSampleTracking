import logging
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.debug)

class ListsPageTest(DatabaseSetup):

    def test_list_home_page_returns_correct_html(self):
        response = self.client.get(f'/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/lists/')
        self.assertContains(response,'Incentive List')
