import logging

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest,wait_for_element
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from django.utils import timezone

MAX_WAIT = 10

class MotherBioSpecimenEcho2EntryTestHairSaliva(FunctionalTest):

    def wait_for_row_in_list_table(self):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_initial_form-collected_not_collected_kit_sent")
                return table
                logging.critical(f"{time.time()}")
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester,child_age=None):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        age_category_fk__age_category=child_age)
        return caregiverbio.pk


    def test_user_can_choose_status_of_hair_or_saliva_information_chooses_kit_sent_collected_shipped_msu_then_echo(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected_kit_sent = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_kit_sent'))
        collected_not_collected_kit_sent.select_by_visible_text('Kit Sent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees kit sent form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Kit sent date:', body_text)

        kit_sent_date = self.browser.find_element(By.ID,"id_kit_sent_form-kit_sent_date")
        kit_sent_date.clear()
        kit_sent_date.send_keys('2023-09-27')

        biospecimen_id = self.browser.find_element(By.ID,'id_kit_sent_form-echo_biospecimen_id')
        biospecimen_id.send_keys('5555555')

        submit = self.browser.find_element(By.XPATH,'//*[@id="kit_sent_form"]/form/input[2]')
        submit.click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Sept. 27, 2023',body_text)

        #user sees collected form on next page

        collected_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Collected', collected_form)
        self.assertNotIn('Incentive date', collected_form)

        #user submits form and sees data

        in_person_remote = Select(self.browser.find_element(By.ID, 'id_hair_saliva_form-in_person_remote'))
        in_person_remote.select_by_visible_text('In Person')

        collected = self.browser.find_element(By.ID,"id_hair_saliva_form-date_collected")
        collected.clear()
        collected.send_keys('2023-09-27')

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Collected Date Time: Sept. 27, 2023', body)

        #User sees incentive form

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Incentive Form',form)

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.clear()
        incentive_date.send_keys('2023-09-03')

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Incentive Date: Sept. 3, 2023', body)

        #user sees shipped to msu form

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped to MSU',form)

        self.assertNotIn('Shipped to WSU',form)
        self.assertNotIn('Shipped to Echo',form)
        date_time_shipped = self.browser.find_element(By.ID,'id_shipped_to_msu_form-shipped_date_time')
        date_time_shipped.send_keys('2023-10-20 09:17:07')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_msu"]/form/input[2]')

        submit.click()

        #user sees shipped to echo data

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped Date Time: Oct. 20, 2023, 9:17 a.m.', body)

        #use sees received at MSU Form

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Received at MSU',form)

        self.assertNotIn('Shipped to WSU',form)
        self.assertNotIn('Shipped to Echo',form)
        date_time_received = self.browser.find_element(By.ID,'id_received_at_msu_form-received_date_time')
        date_time_received.send_keys('2023-10-20 09:17:07')

        submit = self.browser.find_element(By.XPATH,'//*[@id="received_at_msu"]/form/input[2]')

        submit.click()

        #user sees received at MSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Received Date Time: Oct. 20, 2023, 9:17 a.m.', body)

        #user sees shipped to echo form

        body = self.browser.find_element(By.TAG_NAME,'body').text
        needed_div = self.browser.find_element(By.ID,'shipped_to_echo_form').text

        self.assertIn('Shipped to ECHO Form',needed_div)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_echo_form-shipped_date_and_time")
        shipped_date_time.clear()
        shipped_date_time.send_keys('2023-10-20 09:17:07')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_echo_form"]/form/input[2]')

        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped Date Time: Oct. 20, 2023, 9:17 a.m.',body)


    def test_user_can_choose_status_of_hair_or_salvia_information_chooses_not_collected_hope(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)

    def test_user_can_choose_status_of_hair_or_salvia_information_chooses_declined(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        #needed_form = self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_kit_sent')
        # WebDriverWait(self.browser,timeout=50).until(EC.presence_of_element_located((By.ID,'id_initial_form-collected_not_collected_kit_sent')))

        # self.wait_for_row_in_list_table()
        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_kit_sent'))
        #collected_not_collected = Select(wait_for_element(self.browser,'id_initial_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Declined')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Declined', body_text)