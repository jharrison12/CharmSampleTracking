import logging
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)

class ReportsPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(f'/reports/')
        self.assertTemplateUsed(response, 'reports/home.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/reports/')
        self.assertContains(response,'Caregiver Report')


class CaregiverReportPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(f'/reports/caregiver_report/')
        self.assertTemplateUsed(response, 'reports/caregiver_report.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/reports/caregiver_report/')
        self.assertContains(response,'Caregiver Report')

class CaregiverBiospecimenReportPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(f'/reports/biospecimen_report/')
        self.assertTemplateUsed(response, 'reports/biospecimen_report.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/reports/biospecimen_report/')
        self.assertContains(response,'Biospecimen Report')