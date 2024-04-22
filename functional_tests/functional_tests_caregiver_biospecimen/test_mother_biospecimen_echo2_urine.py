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

        form = self.browser.find_element(By.ID, 'collected_information_form').text
        self.assertIn('Collected Form', form)

        # user submits form and sees data

        food_eat_time = self.browser.find_element(By.ID, "id_urine_form-eat_drink_datetime")
        food_eat_time.click()
        self.choose_flatpickr_day(0)

        food_eat_list = self.browser.find_element(By.ID, "id_urine_form-eat_drink_text_field")
        food_eat_list.send_keys('Bread')

        collected = self.browser.find_element(By.ID, "id_urine_form-collected_date_time")
        collected.click()
        time.sleep(2)
        self.choose_flatpickr_day(1)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

    def user_submits_urine_processed(self):

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('bread',body)

    def user_submits_urine_shipped_to_wsu(self):

        #user sees some of the information just entered

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Number of Tubes: 5', body)
        self.assertNotIn('Processed Date Time: None',body)
        self.assertNotIn('Stored Date Time: None', body)
        self.assertNotIn('Number of Tubes: None', body)

        self.assertIn('Logged By:',body)

        #User does not see incentive form

        self.assertNotIn('Incentive', body)

        #user sees shipped to wsu form

        body = self.browser.find_element(By.ID,'shipped_to_wsu_information_form').text
        self.assertIn('Collected Questions',body)
        self.assertIn('If processed and aliquoted off site, under what conditions were the tubes transported to the processing site?',body)

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
        time.sleep(1)
        self.assertIn('Courier: FedEx',body)
        self.assertIn('Shipped By:',body)


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

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}', body)

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
        self.assertNotIn('Declined',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees not collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertIn('Not Collected', body_text)
        self.assertIn('Refused', body_text)
        self.assertIn('Other', body_text)
        ##todo update ft to pass