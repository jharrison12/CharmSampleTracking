import logging
from django.utils import timezone

from biospecimen.models import Caregiver, CaregiverBiospecimen
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

class UrineStaffReport(DatabaseSetup):

    def test_staff_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertTemplateUsed(response, 'reports/biospecimen_report_urine.html')

    def test_staff_urine_report_shows_collected_report_header(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Collected Report')

    def test_staff_urine_report_shows_shipped_to_wsu_report_header(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to WSU Report')

    def test_staff_urine_report_shows_received_at_wsu_report_header(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Received at WSU Report')

    def test_staff_urine_report_shows_shipped_to_echo_report_header(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to Echo Report')

class BloodStaffReport(DatabaseSetup):

    def test_collected_blood_report_returns_correct_html(self):
        response = self.client.get(f'/reports/biospecimen_report/blood/')
        self.assertTemplateUsed(response, 'reports/biospecimen_report_blood.html')

    def test_staff_blood_report_shows_collected_report(self):
        response = self.client.get(f'/reports/biospecimen_report/blood/')
        self.assertContains(response,'Collected Report')

    def test_staff_blood_report_shows_shipped_to_wsu_report(self):
        response = self.client.get(f'/reports/biospecimen_report/blood/')
        self.assertContains(response,'Shipped to WSU Report')

    def test_staff_blood_report_shows_received_at_wsu_report(self):
        response = self.client.get(f'/reports/biospecimen_report/blood/')
        self.assertContains(response,'Received at WSU Report')

    def test_staff_blood_report_shows_shipped_to_echo_report(self):
        response = self.client.get(f'/reports/biospecimen_report/blood/')
        self.assertContains(response,'Shipped to Echo Report')

class CollectedReportUrineTest(DatabaseSetup):

    def test_page_collected_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/collected_report/urine/')
        self.assertTemplateUsed(response, 'reports/collected_report_urine.html')

    def test_collected_urine_report_shows_report_header(self):
        response = self.client.get(f'/reports/collected_report/urine/')
        self.assertContains(response,'Collected Report')

class ShippedtoWSUReportUrineTest(DatabaseSetup):

    def test_page_shipped_to_wsu_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_wsu_report/urine/')
        self.assertTemplateUsed(response, 'reports/shipped_to_wsu_report_urine.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to WSU Report')

class ReceivedatWSUReportUrineTest(DatabaseSetup):

    def test_page_received_at_wsu_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/received_at_wsu_report/urine/')
        self.assertTemplateUsed(response, 'reports/received_at_wsu_report_urine.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Received at WSU Report')

class ShippedtoEchoReportUrineTest(DatabaseSetup):

    def test_page_shipped_to_echo_urine_report_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_echo_report/urine/')
        self.assertTemplateUsed(response, 'reports/shipped_to_echo_report_urine.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/biospecimen_report/urine/')
        self.assertContains(response,'Shipped to Echo Report')

class CollectedReportBloodTest(DatabaseSetup):

    def test_page_collected_blood_report_returns_correct_html(self):
        response = self.client.get(f'/reports/collected_report/blood/')
        self.assertTemplateUsed(response, 'reports/collected_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/collected_report/blood/')
        self.assertContains(response,'Collected Report')

class ShippedtoWSUReportBloodTest(DatabaseSetup):

    def test_page_shipped_to_wsu_blood_report_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_wsu_report/blood/')
        self.assertTemplateUsed(response, 'reports/shipped_to_wsu_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/shipped_to_wsu_report/blood/')
        self.assertContains(response,'Shipped to WSU Report')


class ReceivedatWSUReportBloodTest(DatabaseSetup):

    def test_page_received_at_wsu_blood_report_returns_correct_html(self):
        response = self.client.get(f'/reports/received_at_wsu_report/blood/')
        self.assertTemplateUsed(response, 'reports/received_at_wsu_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/received_at_wsu_report/blood/')
        self.assertContains(response,'Received at WSU Report')

class ShippedtoEchoReportBloodTest(DatabaseSetup):

    def test_page_shipped_to_echo_blood_report_returns_correct_html(self):
        response = self.client.get(f'/reports/shipped_to_echo_report/blood/')
        self.assertTemplateUsed(response, 'reports/shipped_to_echo_report_blood.html')

    def test_page_with_no_specimens_logged_shows_report(self):
        response = self.client.get(f'/reports/shipped_to_echo_report/blood/')
        self.assertContains(response,'Shipped to Echo Report')


class UserRoleReportTest(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester,age_category=None, project='ECHO2'):
        logging.critical(f"charm_id {charm_id} collection_type {collection_type} trimester {trimester} age_category {age_category} project {project}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)

        return caregiverbio.pk

    def initial_send_form_flint(self, primary_key,c_n_or_x,sample_id):
        response = self.client.post(f'/biospecimen/caregiver/{sample_id}/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected": c_n_or_x,
                                          })
        logging.critical(response.status_code)
        return response

    def collected_send_form_flint(self,primary_key,sample_id):
        response = self.client.post(f'/biospecimen/caregiver/{sample_id}/{primary_key}/post/',
                                    data={"urine_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "urine_form-processed_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "urine_form-stored_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "urine_form-number_of_tubes": 5})
        logging.critical(response.status_code)
        return response


    def incentive_send_form(self,primary_key,sampleid):
        response = self.client.post(f'/biospecimen/caregiver/{sampleid}/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })
        return response


    def shipped_to_wsu_send_form(self,primary_key,sampleid):
        response =  self.client.post(f'/biospecimen/caregiver/{sampleid}/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def received_at_wsu_send_form(self,primary_key,sampleid):
        response = self.client.post(f'/biospecimen/caregiver/{sampleid}/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    def login_staff(self):
        self.client.logout()
        self.client.login(**{
            'username':'staff',
            'password':'supersecret'
        })

    def login_detroit(self):
        self.client.logout()
        self.client.login(**{
            'username': 'testuser',
            'password': 'secret'})

    def login_flint(self):
        self.client.logout()
        self.client.login(**{
        'username':'flint_user',
        'password':'super_secret'
        })

    def login_traverse(self):
        self.client.logout()
        self.client.login(**{
    'username':'traverse_user',
    'password':'super_secret'
})

    def test_detroit_user_cannot_see_flint_sample_in_collected_urine_report(self):
        self.login_staff()
        primary_key = self.return_caregiver_bio_pk('4400','U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C','4400')
        self.collected_send_form_flint(primary_key,'4400')
        self.login_detroit()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,'4400')

    def test_detroit_user_cannot_see_traverese_sample_in_collected_urine_report(self):
        self.login_staff()
        traverse_sample='4700'
        primary_key = self.return_caregiver_bio_pk(traverse_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',traverse_sample)
        self.collected_send_form_flint(primary_key,traverse_sample)
        self.login_detroit()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,traverse_sample)

    def test_flint_user_cannot_see_detroit_sample_in_collected_urine_report(self):
        self.login_staff()
        primary_key = self.return_caregiver_bio_pk('4100','U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C','4100')
        self.collected_send_form_flint(primary_key,'4100')
        self.login_flint()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,'4100')

    def test_flint_user_cannot_see_traverse_sample_in_collected_urine_report(self):
        self.login_staff()
        traverse_sample='4700'
        primary_key = self.return_caregiver_bio_pk(traverse_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',traverse_sample)
        self.collected_send_form_flint(primary_key,traverse_sample)
        self.login_flint()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,traverse_sample)

    def test_traverse_user_cannot_see_detroit_sample_in_collected_urine_report(self):
        self.login_staff()
        detroit_sample='4100'
        primary_key = self.return_caregiver_bio_pk(detroit_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',detroit_sample)
        self.collected_send_form_flint(primary_key,detroit_sample)
        self.login_traverse()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,detroit_sample)

    def test_traverse_user_cannot_see_flint_sample_in_collected_urine_report(self):
        self.login_staff()
        flint_sample ='4400'
        primary_key = self.return_caregiver_bio_pk(flint_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',flint_sample)
        self.collected_send_form_flint(primary_key,flint_sample)
        self.login_traverse()
        response = self.client.get(f'/reports/collected_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,flint_sample)

    #Starting with shipped to wsu I am not testing every scenario.  It would take too long

    def test_detroit_user_cannot_see_flint_sample_in_shipped_to_wsu_urine_report(self):
        self.login_staff()
        flint_sample = '4400'
        primary_key = self.return_caregiver_bio_pk(flint_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',flint_sample)
        self.collected_send_form_flint(primary_key,flint_sample)
        self.incentive_send_form(primary_key,flint_sample)
        self.shipped_to_wsu_send_form(primary_key,flint_sample)
        self.login_detroit()
        response = self.client.get(f'/reports/shipped_to_wsu_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,flint_sample)

    def test_flint_user_cannot_see_traverese_sample_in_shipped_to_wsu_urine_report(self):
        self.login_staff()
        sample_id = '4700'
        primary_key = self.return_caregiver_bio_pk(sample_id,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',sample_id)
        self.collected_send_form_flint(primary_key,sample_id)
        self.incentive_send_form(primary_key,sample_id)
        self.shipped_to_wsu_send_form(primary_key,sample_id)
        self.login_flint()
        response = self.client.get(f'/reports/shipped_to_wsu_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,sample_id)

    def test_traverse_user_cannot_see_detroit_sample_in_shipped_to_wsu_urine_report(self):
        self.login_staff()
        sample_id = '4100'
        primary_key = self.return_caregiver_bio_pk(sample_id,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',sample_id)
        self.collected_send_form_flint(primary_key,sample_id)
        self.incentive_send_form(primary_key,sample_id)
        self.shipped_to_wsu_send_form(primary_key,sample_id)
        self.login_traverse()
        response = self.client.get(f'/reports/shipped_to_wsu_report/urine/')
        logging.critical(response.content)
        self.assertNotContains(response,sample_id)


    def test_detroit_user_cannot_see_flint_sample_in_received_at_wsu_urine_report(self):
        self.login_staff()
        flint_sample = '4400'
        primary_key = self.return_caregiver_bio_pk(flint_sample,'U','S')
        logging.critical(f"Primary key {primary_key}")
        self.initial_send_form_flint(primary_key,'C',flint_sample)
        self.collected_send_form_flint(primary_key,flint_sample)
        self.incentive_send_form(primary_key,flint_sample)
        self.shipped_to_wsu_send_form(primary_key,flint_sample)
        self.received_at_wsu_send_form(primary_key,flint_sample)
        self.login_detroit()
        response = self.client.get(f'/reports/received_at_wsu_report/urine/')
        self.assertNotContains(response,flint_sample)