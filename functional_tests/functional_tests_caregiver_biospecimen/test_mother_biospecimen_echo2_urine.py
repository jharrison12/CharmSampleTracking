import logging

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest, TODAY
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class MotherBioSpecimenEcho2EntryTestUrine(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def user_submits_urine_collected(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4101', 'U', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/initial/')

        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4101', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Collected Form', form)

        # user submits form and sees data
        collected = self.browser.find_element(By.ID, "id_urine_form-collected_date_time")
        collected.click()
        new_num = self.choose_flatpickr_day(0)

        processed = self.browser.find_element(By.ID, "id_urine_form-processed_date_time")
        processed.click()
        new_num1 = self.choose_flatpickr_day(new_num)

        stored = self.browser.find_element(By.ID, "id_urine_form-stored_date_time")
        stored.click()
        self.choose_flatpickr_day(new_num1)

        number_of_tubes = self.browser.find_element(By.ID, "id_urine_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

    def user_submits_urine_shipped_to_wsu(self):

        #user sees some of the information just entered

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Number of Tubes: 5', body)

        self.assertIn('Logged By: testuser',body)

        #User sees incentive form

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f'Incentive Date: {TODAY}', body)

        #user sees shipped to wsu form

        body = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped to WSU Form',body)

        #user submits shipped to WSu form
        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.click()
        new_num = self.choose_flatpickr_day(0)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        number_of_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        logged_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-logged_date_time")
        logged_date_time.click()
        self.choose_flatpickr_day(new_num)

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Courier: FedEx',body)
        self.assertIn('Shipped By: testuser',body)


    def user_submits_urine_received_at_wsu(self):
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Received at WSU Form', body)

        # User sees received date time at
        # user submits shipped to WSu form
        received_date_time = self.browser.find_element(By.ID, "id_received_at_wsu_form-received_date_time")
        received_date_time.click()
        self.choose_flatpickr_day(0)


        number_of_tubes = self.browser.find_element(By.ID,'id_received_at_wsu_form-number_of_tubes')
        number_of_tubes.send_keys(5)
        time.sleep(1)
        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Received at WSU: {TODAY}', body)
        self.assertIn(f'Number of Tubes: 5', body)

        # user sees shipped to echo form

    def user_submits_urine_shipped_to_echo(self):
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped to ECHO Form',body)

        shipped_date_time = self.browser.find_element(By.ID, 'id_shipped_to_echo_form-shipped_date_and_time')
        shipped_date_time.click()
        self.choose_flatpickr_day(0)

        number_of_tubes = self.browser.find_element(By.ID, 'id_shipped_to_echo_form-number_of_tubes')
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}', body)
        time.sleep(4)
        self.assertIn(f'Number of Tubes: 5', body)

    def test_user_can_choose_status_of_urine_information_chooses_collected_shipped_wsu(self):
        self.user_submits_urine_collected()
        self.user_submits_urine_shipped_to_wsu()
        self.user_submits_urine_received_at_wsu()
        self.user_submits_urine_shipped_to_echo()

    def test_user_can_choose_status_of_urine_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4101', 'U', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4101', [item.text for item in header_text])
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

    def test_user_can_choose_status_of_urine_information_chooses_declined(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4101', 'U', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4101', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Declined')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Declined', body_text)