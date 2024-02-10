from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest,TODAY
from biospecimen.models import CaregiverBiospecimen,Caregiver,Project
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class MotherBioSpecimenEcho2EntryTestPlacenta(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type):
        echo2 = Project.objects.get(project_name='ECHO2')
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        project_fk=echo2)
        return caregiverbio.pk

    def test_user_can_choose_status_of_placenta_information_chooses_collected_shipped_wsu_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('4100', 'C')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_no_consent'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)

        #user submits form and sees data
        collected = self.browser.find_element(By.ID,"id_placenta_form-collected_date_time")
        collected.click()
        new_num = self.choose_flatpickr_day(0)

        processed = self.browser.find_element(By.ID,"id_placenta_form-processed_date_time")
        processed.click()
        new_num1 = self.choose_flatpickr_day(new_num)

        placed_in_formalin = self.browser.find_element(By.ID,"id_placenta_form-placed_in_formalin")
        placed_in_formalin.click()
        self.choose_flatpickr_day(new_num1)

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        #user sees some of the information just entered

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f'Placed in Formalin: {TODAY}', body)

        self.assertIn('Logged By: testuser',body)

        #User sees incentive form

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f'Incentive Date: {TODAY}', body)

        #user does not see shipped choice form

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertNotIn('Shipped Choice Form',form)

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped to WSU Form',body)
        self.assertNotIn('tubes',body)
        self.assertNotIn('Logged date time:',body)

        #user submits shipped to WSu form
        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.click()
        new_num = self.choose_flatpickr_day(0)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Courier: FedEx',body)
        self.assertIn('Shipped By: testuser',body)
        self.assertNotIn('Number of Tubes',body)

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Received at WSU Form',body)

        #User sees received form
        received_date_time = self.browser.find_element(By.ID,"id_received_at_wsu_form-received_date_time")
        received_date_time.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Received at WSU: {TODAY}', body)

        #User sees shipped to echo form
        shipped_echo_date_time = self.browser.find_element(By.ID,"id_shipped_to_echo_form-shipped_date_and_time")
        shipped_echo_date_time.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        submit.click()

        #User sees shipped to echo data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}',body)



    def test_user_can_choose_status_of_placenta_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('4100', 'C')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_no_consent'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)

    def test_user_can_choose_status_of_placenta_information_chooses_no_consent(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('4100', 'C')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_no_consent'))
        collected_not_collected.select_by_visible_text('No Consent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('No Consent', body_text)