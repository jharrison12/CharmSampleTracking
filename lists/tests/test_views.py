import logging
from biospecimen.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.debug)

class ListsPageTest(DatabaseSetup):

    def test_list_home_page_returns_correct_html(self):
        response = self.client.get(f'/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/lists/')
        self.assertContains(response,'Incentive List')

class IncentiveListPageCaregiverBiospecimen(DatabaseSetup):

    def test_list_home_page_returns_correct_html(self):
        response = self.client.get(f'/lists/incentive_list/caregiver/biospecimen/')
        self.assertTemplateUsed(response, 'lists/incentive_list_caregiver_biospecimen.html')

    def test_incentive_list_contains_p7000_if_biospecimen_at_point_of_incentive_form(self):
        response = self.client.get(f'/lists/incentive_list/caregiver/biospecimen/')
        self.assertContains(response, '4100')

class IncentiveListPageCaregiverCharmID(DatabaseSetup):

    def test_list_home_page_returns_correct_html(self):
        response = self.client.get(f'/lists/incentive_list/caregiver/charm_id/')
        self.assertTemplateUsed(response, 'lists/incentive_list_caregiver_charm_id.html')

    def test_incentive_list_contains_4100_if_biospecimen_at_point_of_incentive_form(self):
        response = self.client.get(f'/lists/incentive_list/caregiver/charm_id/')
        logging.debug(response.content.decode())
        self.assertContains(response, '4100')

    def test_incentive_list_contains_biospecimen_name_if_biospecimen_at_point_of_incentive_form(self):
        response = self.client.get(f'/lists/incentive_list/caregiver/charm_id/')
        self.assertContains(response, 'Hair')