import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone
logging.basicConfig(level=logging.debug)

TODAY = dt.datetime.now().strftime('%b. %d, %Y')

class MotherBioSpecimenEcho2EntryTestBlood(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester,project='ECHO2'):
        logging.debug(f"{charm_id} {collection_type} {trimester}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def user_inputs_first_portion_of_blood_page(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page
        time.sleep(1)
        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)

        #user submits form and sees data
        collected = self.browser.find_element(By.ID,"id_blood_form-collected_date_time")
        collected.click()
        number_of_elements = self.choose_flatpickr_day(0)
        time.sleep(1)

        processed = self.browser.find_element(By.ID,"id_blood_form-processed_date_time")
        processed.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        stored = self.browser.find_element(By.ID,"id_blood_form-stored_date_time")
        stored.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        #user sees a ton of checkboxes for all the bloods possible
        #user does not see whole blood number of tubes until whole blood is checked

        body = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertNotIn('Number of Tubes:',body)
        self.assertIn('Plasma',body)
        self.assertIn('Whole Blood',body)
        self.assertIn('Serum',body)
        self.assertIn('Red Blood Cells',body)
        self.assertIn('Buffy Coat',body)


        whole_blood_checkbox = self.browser.find_element(By.ID,"id_blood_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_blood_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Whole Blood Number of Tubes: 3', body)
        self.assertNotIn('Plasma Number of Tubes', body)

        #user sees incentive form

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Incentive Form',form)

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f"Incentive Date: {dt.datetime.now().strftime('%b. %d, %Y')}", body)

        #user submits shipped to WSu form

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        logged_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-logged_date_time")
        logged_date_time.click()
        self.choose_flatpickr_day(number_of_elements)

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        #User sees a bunch of check boxes without number of tubes
        shipped_div = self.browser.find_element(By.ID, 'shipped_to_wsu_information_form').text

        self.assertNotIn('Number of Tubes:', shipped_div)
        self.assertIn('Plasma', shipped_div)
        self.assertIn('Whole Blood', shipped_div)
        self.assertIn('Serum', shipped_div)
        self.assertIn('Red Blood Cells', shipped_div)
        self.assertIn('Buffy Coat', shipped_div)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-whole_blood")
        whole_blood_checkbox.click()


    def test_user_can_choose_status_of_blood_information_chooses_collected_shipped_wsu(self):
        self.user_inputs_first_portion_of_blood_page()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        shipped_div = self.browser.find_element(By.ID, 'shipped_to_wsu_information_form').text
        self.assertIn('Number of Tubes:', shipped_div)

        ##TODO implement code check that tubes match number of tubes previously entered
        ##TODO implement code that sends email or alerts staff if this happens?

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        needed_div = self.browser.find_element(By.ID,'shipped_to_wsu_information').text
        self.assertIn('Courier: FedEx',needed_div)

        #user sees that whole blood check box is clicked

        self.assertIn("Blood",needed_div)

        #User sees received date time at
        #user submits received at WSU form
        received_date_time = self.browser.find_element(By.ID,"id_received_at_wsu_form-received_date_time")
        received_date_time.click()
        time.sleep(2)
        self.choose_flatpickr_day(0)

        #User sees a bunch of check boxes without number of tubes
        received_div = self.browser.find_element(By.ID, 'received_at_wsu_information_form').text
        whole_blood_number_of_tubes_text = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood_number_of_tubes").text

        self.assertNotIn('Number of Tubes:', whole_blood_number_of_tubes_text)
        self.assertIn('Plasma', received_div)
        self.assertIn('Whole Blood', received_div)
        self.assertIn('Serum', received_div)
        self.assertIn('Red Blood Cells', received_div)
        self.assertIn('Buffy Coat', received_div)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();",submit)
        self.browser.execute_script("arguments[0].click();",submit)
        #submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Received at WSU {TODAY}', body)

        #User sees shipped to Echo form

        shipped_echo_date_time = self.browser.find_element(By.ID,'id_shipped_to_echo_form-shipped_date_and_time')
        shipped_echo_date_time.click()
        self.choose_flatpickr_day(0)

        whole_blood_number_of_tubes_text = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes").text
        self.assertNotIn('Number of Tubes:', whole_blood_number_of_tubes_text)
        self.assertIn('Plasma', body)
        self.assertIn('Whole Blood', body)
        self.assertIn('Serum', body)
        self.assertIn('Red Blood Cells', body)
        self.assertIn('Buffy Coat', body)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();", submit)
        self.browser.execute_script("arguments[0].click();", submit)

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}',body)


    def test_user_can_choose_status_of_blood_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B', trimester='S')
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

    def test_user_can_choose_status_of_blood_information_chooses_declined(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B',trimester='S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
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

    def test_user_can_submited_blood_collected_information_and_then_leaves_and_returns_and_incentive_form_is_there(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
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
        collected = self.browser.find_element(By.ID, "id_blood_form-collected_date_time")
        collected.click()
        time.sleep(2)
        new_selector  = self.choose_flatpickr_day(number_of_css_selector=0)

        processed = self.browser.find_element(By.ID, "id_blood_form-processed_date_time")
        processed.click()
        new_selector=self.choose_flatpickr_day(number_of_css_selector=new_selector)

        stored = self.browser.find_element(By.ID, "id_blood_form-stored_date_time")
        stored.click()
        self.choose_flatpickr_day(number_of_css_selector=new_selector)

        # user sees a ton of checkboxes for all the bloods possible
        # user does not see whole blood number of tubes until whole blood is checked

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertNotIn('Number of Tubes:', body)
        self.assertIn('Plasma', body)
        self.assertIn('Whole Blood', body)
        self.assertIn('Serum', body)
        self.assertIn('Red Blood Cells', body)
        self.assertIn('Buffy Coat', body)

        whole_blood_checkbox = self.browser.find_element(By.ID, "id_blood_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID, "id_blood_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Whole Blood Number of Tubes: 3', body)
        self.assertNotIn('Plasma Number of Tubes', body)

        # user sees incentive form
        self.browser.implicitly_wait(2)
        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Incentive Form', form)
        time.sleep(2)

        incentive_date = self.browser.find_element(By.ID, 'id_incentive_form-incentive_date')

        self.browser.get(f'{self.live_server_url}/biospecimen/')

        time.sleep(2)
        self.browser.get(f'{self.live_server_url}/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        time.sleep(2)
        # is incentive form still there?

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Incentive Form', form)

        incentive_date = self.browser.find_element(By.ID, 'id_incentive_form-incentive_date')
        incentive_date.click()
        self.choose_flatpickr_day(0)


    def test_user_submits_incorrect_number_of_tubes_and_error_is_thrown(self):
        self.user_inputs_first_portion_of_blood_page()
        whole_blood_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(4)

        #check that modal text isn't in body
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Whole Blood number of tubes entered 4 does not match number of Whole Blood collected tubes: 3',
                      body_text)

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()
        WebDriverWait(self.browser,5).until(EC.visibility_of_element_located((By.ID
                                                                                  ,'exampleModal')))
        modal_text = self.browser.find_element(By.ID,'exampleModal').text

        self.assertIn('Whole Blood number of tubes entered 4 does not match number of Whole Blood collected tubes: 3',modal_text)

        #user clicks cancel
        time.sleep(2)
        self.browser.find_element(By.ID,'modal_cancel_button').click()

        #user resubmits shipped to WSu form

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        logged_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-logged_date_time")
        logged_date_time.click()
        self.choose_flatpickr_day(number_of_elements)

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        #User sees a bunch of check boxes without number of tubes
        shipped_div = self.browser.find_element(By.ID, 'shipped_to_wsu_information_form').text

        self.assertNotIn('Number of Tubes:', shipped_div)
        self.assertIn('Plasma', shipped_div)
        self.assertIn('Whole Blood', shipped_div)
        self.assertIn('Serum', shipped_div)
        self.assertIn('Red Blood Cells', shipped_div)
        self.assertIn('Buffy Coat', shipped_div)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID, "id_shipped_to_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user submits wrong number to received at WSU form and sees modal

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(4)

        #check that modal text isn't in body
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Whole Blood number of tubes entered 4 does not match number of Whole Blood shipped to wsu tubes: 3',
                      body_text)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();",submit)
        self.browser.execute_script("arguments[0].click();",submit)

        WebDriverWait(self.browser,5).until(EC.visibility_of_element_located((By.ID
                                                                                  ,'exampleModal')))
        modal_text = self.browser.find_element(By.ID,'exampleModal').text

        self.assertIn('Whole Blood number of tubes entered 4 does not match number of Whole Blood shipped to wsu tubes: 3',
                      modal_text)

        # user clicks cancel renters correct number
        time.sleep(2)
        self.browser.find_element(By.ID, 'modal_cancel_button').click()

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_received_at_wsu_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();",submit)
        self.browser.execute_script("arguments[0].click();",submit)

        body = self.browser.find_element(By.TAG_NAME,'Body')

        #User sees shipped to Echo form
        #check that modal isnt in body
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn(
            'Whole Blood number of tubes entered 4 does not match number of Whole Blood received at wsu tubes: 3',
            body_text)

        shipped_echo_date_time = self.browser.find_element(By.ID,'id_shipped_to_echo_form-shipped_date_and_time')
        shipped_echo_date_time.click()
        self.choose_flatpickr_day(0)

        whole_blood_number_of_tubes_text = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes").text
        self.assertNotIn('Number of Tubes:', whole_blood_number_of_tubes_text)
        self.assertIn('Plasma', body_text)
        self.assertIn('Whole Blood', body_text)
        self.assertIn('Serum', body_text)
        self.assertIn('Red Blood Cells', body_text)
        self.assertIn('Buffy Coat', body_text)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood")
        whole_blood_checkbox.click()
        # user sends wrong number of tubes and gets modal
        whole_blood_tubes = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(4)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();", submit)
        self.browser.execute_script("arguments[0].click();", submit)

        WebDriverWait(self.browser,5).until(EC.visibility_of_element_located((By.ID
                                                                                  ,'exampleModal')))
        modal_text = self.browser.find_element(By.ID,'exampleModal').text

        self.assertIn('Whole Blood number of tubes entered 4 does not match number of Whole Blood received at wsu tubes: 3',
                      modal_text)

        self.browser.find_element(By.ID, 'modal_cancel_button').click()

        shipped_echo_date_time = self.browser.find_element(By.ID,'id_shipped_to_echo_form-shipped_date_and_time')
        shipped_echo_date_time.click()
        self.choose_flatpickr_day(0)

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        whole_blood_number_of_tubes_text = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes").text
        self.assertNotIn('Number of Tubes:', whole_blood_number_of_tubes_text)
        self.assertIn('Plasma', body_text)
        self.assertIn('Whole Blood', body_text)
        self.assertIn('Serum', body_text)
        self.assertIn('Red Blood Cells', body_text)
        self.assertIn('Buffy Coat', body_text)

        whole_blood_checkbox = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID,"id_shipped_to_echo_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        self.browser.execute_script("arguments[0].scrollIntoView();", submit)
        self.browser.execute_script("arguments[0].click();", submit)

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}',body)
