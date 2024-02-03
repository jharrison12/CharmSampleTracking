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

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk


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

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.get(f'{self.browser.current_url}no_specimen_report/')

        text = self.webpage_text()

        self.assertIn('4100', text)

        self.browser.find_element(By.LINK_TEXT,'4100').click()

        text = self.webpage_text()

        self.assertIn('Trimester',text)


    def test_user_enters_specimen_and_doesnt_see_id_on_no_specimen_report(self):
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
        ##TODO implement print function

    def test_user_can_see_shipped_to_wsu_urine_report(self):
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Shipped to WSU Urine Report').click()

        text = self.webpage_text()

        self.assertIn('4101', text)

        # user sees a urine that is collected

        self.assertIn('12UR410101', text)

        self.assertIn('Number of Tubes', text)

        ##TODO implement search bar
        ##TODO implement print function


    def test_user_can_see_recieved_at_wsu_urine_report(self):
        motherurine.user_submits_urine_collected(self)
        motherurine.user_submits_urine_shipped_to_wsu(self)
        motherurine.user_submits_urine_received_at_wsu(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Received at WSU Urine Report').click()

        text = self.webpage_text()

        self.assertIn('4101', text)

        # user sees a urine that is collected

        self.assertIn('12UR410101', text)

        self.assertIn('Number of Tubes', text)
        self.assertIn('5', text)


        ##TODO implement search bar
        ##TODO implement print function

    def test_user_can_see_collected_blood_report(self):
        motherblood.user_input_collected_blood(self)

        # User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.find_element(By.LINK_TEXT, 'Collected Report Blood').click()

        text = self.webpage_text()

        self.assertIn('4100', text)

        # user sees a urine that is collected

        self.assertIn('12BL410001', text)

        self.assertIn('Whole Blood', text)

        ##todo implement search bar
        ##TODO implement print function

    def test_user_can_see_shipped_to_wsu_blood_report(self):
        motherblood.user_input_collected_blood(self)
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

        # user sees a urine that is collected

        self.assertIn('12BL410001', text)

        self.assertIn('Whole Blood', text)
        self.assertIn('Shipped to WSU Report', text)

        ##todo implement search bar
        ##TODO implement print function

    def test_user_can_see_received_at_wsu_blood_report(self):
        motherblood.user_input_collected_blood(self)
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

        ##todo implement search bar
        ##TODO implement print function
