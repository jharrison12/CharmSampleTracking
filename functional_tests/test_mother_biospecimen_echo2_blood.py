import logging

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone
logging.basicConfig(level=logging.CRITICAL)

class MotherBioSpecimenEcho2EntryTestBlood(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester,project='ECHO2'):
        logging.debug(f"{charm_id} {collection_type} {trimester}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def test_user_can_choose_status_of_blood_information_chooses_collected_shipped_wsu(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)

        #user submits form and sees data
        collected = self.browser.find_element(By.ID,"id_blood_form-collected_date_time")
        collected.clear()
        collected.send_keys('2023-09-27 12:52:26')

        stored = self.browser.find_element(By.ID,"id_blood_form-stored_date_time")
        stored.send_keys('2023-09-27 12:52:26')

        processed = self.browser.find_element(By.ID,"id_blood_form-processed_date_time")
        processed.send_keys('2023-09-27 12:52:26')

        number_of_tubes = self.browser.find_element(By.ID,"id_blood_form-number_of_tubes")
        number_of_tubes.send_keys(5)


        #user sees a ton of checkboxes for all the bloods possible

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_blood_form-whole_blood")

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()


        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Number of Tubes: 5', body)

        #user sees option to choose shipped to wsu or shipped to echo

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped Choice Form',form)

        shipped_to_wsu = Select(self.browser.find_element(By.ID,'id_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_to_wsu.select_by_visible_text('Shipped to WSU')
        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_choice"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped to WSU Form',body)

        #user submits shipped to WSu form
        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.clear()
        shipped_date_time.send_keys('2023-09-27 12:52:26')

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        number_of_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        logged_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-logged_date_time")
        logged_date_time.send_keys('2023-09-27 12:52:26')

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Courier: FedEx',body)

    def test_user_can_choose_status_of_blood_information_chooses_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', trimester='F')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)

        #user submits form and sees data
        collected = self.browser.find_element(By.ID,"id_blood_form-collected_date_time")
        collected.clear()
        collected.send_keys('2023-09-27 12:52:26')

        stored = self.browser.find_element(By.ID,"id_blood_form-stored_date_time")
        stored.send_keys('2023-09-27 12:52:26')

        processed = self.browser.find_element(By.ID,"id_blood_form-processed_date_time")
        processed.send_keys('2023-09-27 12:52:26')

        number_of_tubes = self.browser.find_element(By.ID,"id_blood_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Number of Tubes: 5', body)

        #user sees option to choose shipped to wsu or shipped to echo

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped Choice Form',form)

        shipped_to_echo = Select(self.browser.find_element(By.ID,'id_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_to_echo.select_by_visible_text('Shipped to Echo')
        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_choice"]/form/input[2]')
        submit.click()


        body = self.browser.find_element(By.TAG_NAME,'body').text
        needed_div = self.browser.find_element(By.ID,'shipped_to_echo_information').text
        self.assertIn('Shipped to Echo:',needed_div)


    def test_user_can_choose_status_of_blood_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)

    def test_user_can_choose_status_of_blood_information_chooses_no_consent(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')
        time.sleep(60)
        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('No Consent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('No Consent', body_text)