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

class CaregiverBiospcimenIDSwithNoLoggedSpecimensTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/no_specimen_report/')
        self.assertTemplateUsed(response, 'reports/no_specimen_report.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/no_specimen_report/')
        self.assertContains(response,'No Biospecimen Report')

class CollectedReportUrineTest(DatabaseSetup):

    def test_collected_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertTemplateUsed(response, 'reports/biospecimen_report_urine.html')

    def test_collected_urine_report_shows_report_header(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Collected Report')

class ShippedtoWSUReportUrineTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to WSU Report')

class ReceivedatWSUReportUrineTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Received at WSU Report')

class ShippedtoEchoReportUrineTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to Echo Report')

class CollectedReportBloodTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/collected_report/blood/')
        self.assertTemplateUsed(response, 'reports/collected_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/collected_report/blood/')
        self.assertContains(response,'Collected Report')

class ShippedtoWSUReportBloodTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_wsu_report/blood/')
        self.assertTemplateUsed(response, 'reports/shipped_to_wsu_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/shipped_to_wsu_report/blood/')
        self.assertContains(response,'Shipped to WSU Report')


class ReceivedatWSUReportBloodTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/received_at_wsu_report/blood/')
        self.assertTemplateUsed(response, 'reports/received_at_wsu_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/received_at_wsu_report/blood/')
        self.assertContains(response,'Received at WSU Report')

class ShippedtoEchoReportBloodTest(DatabaseSetup):

    def test_page_with_no_specimens_logged_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_echo_report/blood/')
        self.assertTemplateUsed(response, 'reports/shipped_to_echo_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/shipped_to_echo_report/blood/')
        self.assertContains(response,'Shipped to Echo Report')
