import logging
from biospecimen.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.debug)

class ReportsPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(f'/reports/')
        self.assertTemplateUsed(response, 'reports/home.html')

class CaregiverBiospecimenReportPageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(f'/reports/biospecimen_report/')
        self.assertTemplateUsed(response, 'reports/biospecimen_report.html')

    def test_home_page_contains_caregiver_reports(self):
        response = self.client.get(f'/reports/biospecimen_report/')
        self.assertContains(response,'Biospecimen Report')

class CaregiverBiospcimenIDSwithNoLoggedSpecimens(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/no_specimen_report/')
        self.assertTemplateUsed(response, 'reports/no_specimen_report.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/no_specimen_report/')
        self.assertContains(response,'No Biospecimen Report')