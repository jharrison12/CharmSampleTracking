import datetime
import logging
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

from biospecimen.models import Caregiver, CaregiverBiospecimen
from functional_tests.base import FunctionalTest
from selenium.webdriver.support.ui import Select
from functional_tests.functional_tests_caregiver_biospecimen.test_mother_biospecimen_echo2_urine import MotherBioSpecimenEcho2EntryTestUrine as motherurine
from functional_tests.functional_tests_caregiver_biospecimen.test_mother_biospecimen_echo2_blood import MotherBioSpecimenEcho2EntryTestBlood as motherblood


class ReportsPageTest(FunctionalTest):
    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def logout(self):
        self.browser.find_element(By.ID,'logout_button').click()

    def login_staff(self):
        self.logout()
        self.browser.find_element(By.LINK_TEXT,'Login').click()
        self.browser.find_element(By.ID,'id_username').send_keys('staff')
        self.browser.find_element(By.ID,'id_password').send_keys('supersecret')
        self.browser.find_element(By.ID,'login_button').click()

    def test_user_can_see_biospecimen_report(self):
        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.get(f'{self.browser.current_url}biospecimen_report/')

        text = self.webpage_text()

        self.assertIn('4100',text)


    def test_user_can_see_no_specimen_report(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')
        self.login_staff()
        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT,'Reports').click()
        self.browser.find_element(By.LINK_TEXT,'Charm IDS with no biospecimen').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        self.browser.find_element(By.LINK_TEXT,'4100').click()

        text = self.webpage_text()

        self.assertIn('Trimester',text)


    def test_user_enters_specimen_and_doesnt_see_id_on_no_specimen_report(self):
        self.login_staff()
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)

        self.browser.find_element(By.LINK_TEXT, 'Charm IDS with no biospecimen').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        self.browser.find_element(By.LINK_TEXT,'4100').click()

        text = self.webpage_text()

        self.assertIn('Trimester',text)

        self.browser.find_element(By.LINK_TEXT,'Urine 4100 (12UR410001)').click()

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)

        self.browser.get(self.live_server_url)

        self.browser.get(f'{self.browser.current_url}reports/no_specimen_report/')

        text = self.webpage_text()

        self.assertNotIn('4100',text)

class StaffUrineReportPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def logout(self):
        self.browser.find_element(By.ID,'logout_button').click()

    def login_staff(self):
        self.logout()
        self.browser.find_element(By.LINK_TEXT,'Login').click()
        self.browser.find_element(By.ID,'id_username').send_keys('staff')
        self.browser.find_element(By.ID,'id_password').send_keys('supersecret')
        self.browser.find_element(By.ID,'login_button').click()

    def test_user_can_see_staff_collected_urine_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Collected Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4101',text)
        self.assertNotIn('12UR410101',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'collected_report_header').click()
        text = self.webpage_text()
        self.assertIn('Collected Date',text)
        self.assertIn('Eat Drink Date',text)
        self.assertIn('Eat Drink Notes',text)
        self.assertIn('Notes and Deviations',text)

        #User clicks on header to hide report
        self.browser.find_element(By.ID,'collected_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4101',text)
        self.assertNotIn('12UR410101',text)

        ##TODO implement search bar

    def test_user_can_see_staff_processed_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Processed Report',text)
        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4101',text)
        self.assertNotIn('12UR410101',text)

        #user clicks on report header
        self.browser.find_element(By.ID,'processed_report_header').click()
        text = self.webpage_text()
        self.assertIn('Processed Date',text)
        self.assertIn('All 18ml Vials Collected?',text)
        self.assertIn('18ml Estimated Volume',text)
        self.assertIn('18ml Aliquots Collected',text)
        self.assertIn('All 7ml Collected?',text)
        self.assertIn('7ml Estimated Volume',text)
        self.assertIn('7ml Aliquots Collected',text)
        self.assertIn('Notes and Deviations',text)
        self.assertIn('1.1',text)
        self.assertIn('2',text)

    def test_user_can_see_staff_frozen_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Frozen Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4101',text)
        self.assertNotIn('12UR410101',text)
        #user clicks on report header
        self.browser.find_element(By.ID,'frozen_report_header').click()
        text = self.webpage_text()

        self.assertIn('Freezer Placed Date',text)
        self.assertIn('Number of Tubes',text)
        self.assertIn('Notes',text)
        self.assertIn('2',text)
        self.assertIn('they were really cold',text)


    def test_user_can_see_staff_shipped_to_wsu_urine_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Shipped to WSU Report', text)
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)

        self.browser.find_element(By.ID, 'shipped_to_wsu_report_header').click()

        text = self.webpage_text()
        self.assertIn('4101', text)
        self.assertIn('12UR410101', text)
        self.assertIn('Number of Tubes', text)
        self.assertIn('5', text)

        self.browser.find_element(By.ID, 'shipped_to_wsu_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)
        self.assertNotIn('Number of Tubes', text)
        self.assertNotIn('5', text)


    def test_user_can_see_staff_recieved_at_wsu_urine_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)
        motherurine.user_submits_urine_received_at_wsu(self)

        # User visits the page for P7000
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Received at WSU Report', text)
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)

        self.browser.find_element(By.ID,'received_at_wsu_report_header').click()

        text = self.webpage_text()
        self.assertIn('4101', text)
        self.assertIn('12UR410101', text)

        self.browser.find_element(By.ID,'received_at_wsu_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)

        ##TODO implement search bar

    def test_user_can_see_staff_shipped_to_echo_urine_report(self):
        self.login_staff()
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)
        motherurine.user_submits_urine_received_at_wsu(self)
        motherurine.user_submits_urine_shipped_to_echo(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Urine').click()

        text = self.webpage_text()
        self.assertIn('Shipped to Echo Report', text)
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)

        self.browser.find_element(By.ID, 'shipped_to_echo_report_header').click()

        text = self.webpage_text()
        self.assertIn('4101', text)
        self.assertIn('12UR410101', text)
        self.assertNotIn('Number of Tubes', text)

        self.browser.find_element(By.ID, 'shipped_to_echo_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4101', text)
        self.assertNotIn('12UR410101', text)
        self.assertNotIn('Number of Tubes', text)
        self.assertNotIn('5', text)
        
        ##TODO implement search bar

    def test_detroit_flint_and_traverse_user_cannot_see_staff_reports(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertNotIn('Biospecimen Report Urine',text)
        self.assertNotIn('Biospecimen Report Blood',text)
        self.assertNotIn('Charm IDS with no biospecimen',text)

        #todo add flint and traverse


class StaffBloodReportPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def logout(self):
        self.browser.find_element(By.ID,'logout_button').click()

    def login_staff(self):
        self.logout()
        self.browser.find_element(By.LINK_TEXT,'Login').click()
        self.browser.find_element(By.ID,'id_username').send_keys('staff')
        self.browser.find_element(By.ID,'id_password').send_keys('supersecret')
        self.browser.find_element(By.ID,'login_button').click()


    def test_user_can_see_collected_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()
        self.assertIn('Reports',text)

        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Collected Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'collected_report_header').click()
        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('Collected Date',text)
        self.assertIn('Eat/Drink Date',text)
        self.assertIn('Tube #1 Partial/Complete',text)
        self.assertIn('Tube #1 Blood Type',text)
        self.assertIn('Tube #1 Hemolysis',text)
        self.assertIn('Tube #1 Estimated Volume',text)
        self.assertIn('Tube #2 Partial/Complete',text)
        self.assertIn('Tube #2 Blood Type',text)
        self.assertIn('Tube #2 Hemolysis',text)
        self.assertIn('Tube #2 Estimated Volume',text)
        self.assertIn('Tube #3 Partial/Complete',text)
        self.assertIn('Tube #3 Blood Type',text)
        self.assertIn('Tube #3 Hemolysis',text)
        self.assertIn('Tube #3 Estimated Volume',text)
        self.assertIn('Partial',text)
        self.assertIn('Mild',text)
        self.assertIn('EDTA',text)
        self.assertIn('Serum',text)


        #User clicks on header to hide report
        self.browser.find_element(By.ID,'collected_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)
        self.assertNotIn('Hemolysis',text)

        ##TODO implement search bar


    def test_user_can_see_processed_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()
        self.assertIn('Reports',text)

        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Blood').click()
        time.sleep(10)
        text = self.webpage_text()
        self.assertIn('Processed Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'processed_report_header').click()
        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('Process Date',text)
        self.assertIn('Eat/Drink Date',text)


        #User clicks on header to hide report
        self.browser.find_element(By.ID,'collected_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)
        self.assertNotIn('Hemolysis',text)

        ##TODO implement search bar

    def test_user_can_see_shipped_to_wsu_blood_staff_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Shipped to WSU Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'shipped_to_wsu_report_header').click()
        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('12BL410001',text)
        self.assertIn('3',text)

        #User clicks on header to hide report
        self.browser.find_element(By.ID,'shipped_to_wsu_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)
        self.assertIn('3',text)

        ##TODO implement search bar

    def test_user_can_see_received_at_wsu_blood_staff_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)
        motherblood.user_inputs_received_at_wsu_blood(self)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Received at WSU Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'received_at_wsu_report_header').click()
        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('12BL410001',text)
        self.assertIn('3',text)

        #User clicks on header to hide report
        self.browser.find_element(By.ID,'received_at_wsu_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)
        self.assertIn('3',text)

        ##TODO implement search bar

    def test_user_can_see_shipped_to_echo_blood_staff_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)
        motherblood.user_inputs_received_at_wsu_blood(self)
        motherblood.user_inputs_shipped_echo_blood_page(self)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Biospecimen Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Shipped to Echo Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)

        #User clicks on the header and it shows report
        self.browser.find_element(By.ID,'shipped_to_echo_report_header').click()
        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('12BL410001',text)
        self.assertIn('3',text)

        #User clicks on header to hide report
        self.browser.find_element(By.ID,'shipped_to_echo_report_header').click()
        text = self.webpage_text()
        self.assertNotIn('4100',text)
        self.assertNotIn('12BL410001',text)
        self.assertIn('3',text)

        ##TODO implement search bar

class UrineReportsPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def test_user_can_see_collected_urine_report(self):
        motherurine.user_submits_urine_collected(self)

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.find_element(By.LINK_TEXT, 'Collected Report Urine').click()

        text = self.webpage_text()

        self.assertIn('4101',text)

        #user sees a urine that is collected

        self.assertIn('12UR410101',text)

        self.assertIn('Number of Tubes',text)
        
        ##TODO implement search bar


    def test_user_can_see_shipped_to_wsu_urine_report(self):
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Shipped to WSU Report Urine').click()

        text = self.webpage_text()

        self.assertIn('4101', text)

        # user sees a urine that is collected

        self.assertIn('12UR410101', text)

        self.assertIn('Number of Tubes', text)
        
        ##TODO implement search bar

    def test_user_can_see_recieved_at_wsu_urine_report(self):
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)
        motherurine.user_submits_urine_received_at_wsu(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Received at WSU Report Urine').click()

        text = self.webpage_text()

        self.assertIn('4101', text)

        # user sees a urine that is collected

        self.assertIn('12UR410101', text)

        self.assertIn('Number of Tubes', text)
        self.assertIn('5', text)
        
        ##TODO implement search bar


    def test_user_can_see_shipped_to_echo_urine_report(self):
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_processed(self)
        motherurine.user_submits_urine_frozen(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)
        motherurine.user_submits_urine_received_at_wsu(self)
        motherurine.user_submits_urine_shipped_to_echo(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Shipped to Echo Report Urine').click()

        text = self.webpage_text()

        self.assertIn('4101', text)

        # user sees a urine that is collected

        self.assertIn('12UR410101', text)

        self.assertNotIn('Number of Tubes', text)

        
        ##TODO implement search bar


class BloodReportsPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def logout(self):
        self.browser.find_element(By.ID,'logout_button').click()

    def login_staff(self):
        self.logout()
        self.browser.find_element(By.LINK_TEXT,'Login').click()
        self.browser.find_element(By.ID,'id_username').send_keys('staff')
        self.browser.find_element(By.ID,'id_password').send_keys('supersecret')
        self.browser.find_element(By.ID,'login_button').click()

    def test_user_can_see_collected_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)

        # User visits the page for 4100
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Collected Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Collected Report',text)

        #4101 Should not be seen because it is hidden by javascript
        self.assertNotIn('4101',text)
        self.assertNotIn('12BL410101',text)

        #User clicks on the header and it shows report

        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('12BL410001',text)
        self.assertIn('3',text)

    def test_user_can_see_processed_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)

        #User visits the page for 4100
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Processed Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Processed Report',text)

        text = self.webpage_text()
        self.assertIn('4100',text)
        self.assertIn('12BL410001',text)
        self.assertIn('3',text)

    def test_user_can_see_frozen_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)

        text = self.webpage_text()

        #User visits the page for 4100
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Frozen Report Blood').click()

        text = self.webpage_text()
        self.assertIn('Frozen Report', text)

        text = self.webpage_text()
        self.assertIn(datetime.datetime.today().strftime('%B %#d, %Y'), text)
        self.assertIn('4100', text)
        self.assertIn('12BL410001', text)
        self.assertIn('3', text)


    def test_user_can_see_shipped_to_wsu_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)
        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Shipped to WSU Report Blood').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        # user sees a blood that is collected

        self.assertIn('12BL410001', text)

        self.assertIn('Whole Blood', text)
        self.assertIn('Shipped to WSU Report', text)
        self.assertIn('Shipped Date', text)
        

        ##todo implement search bar

    def test_user_can_see_received_at_wsu_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)
        motherblood.user_inputs_received_at_wsu_blood(self)
        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Received at WSU Report Blood').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        # user sees a urine that is collected

        self.assertIn('12BL410001', text)

        self.assertIn('Whole Blood', text)
        self.assertIn('Received at WSU Report', text)
        self.assertIn('3', text)
        
        ##todo implement search bar


    def test_user_can_see_shipped_to_echo_blood_report(self):
        self.login_staff()
        motherblood.user_input_collected_blood(self)
        motherblood.user_inputs_processed_blood_information(self)
        motherblood.user_inputs_frozen_information(self)
        motherblood.user_inputs_shipped_to_wsu_blood(self)
        motherblood.user_inputs_received_at_wsu_blood(self)
        motherblood.user_inputs_shipped_echo_blood_page(self)
        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Shipped to Echo Blood Report').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        # user sees a urine that is collected

        self.assertIn('12BL410001', text)

        self.assertNotIn('Whole Blood', text)
        self.assertNotIn('Serum', text)
        self.assertNotIn('Bloodspots', text)
        self.assertIn('Shipped to Echo Report', text)

        
        ##todo implement search bar
