from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time
import datetime
from selenium.webdriver.support.ui import Select

class MotherBioSpecimenBloodspotsTest(FunctionalTest):

    def test_user_can_see_bio_blood_spot_information(self):
        # User visits the caregiver biospecimen page and sees urine
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/blood_spots/')

        header_text = self.browser.find_elements(By.TAG_NAME,'h1')
        self.assertIn('Charm ID: P7000 Family ID: 4444',[item.text for item in header_text])

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn("ID: 1111BS", body)
        self.assertIn("Log Status: Completed", body)

        #User sees processed information if there is processed data
        self.assertIn('Collected Date Time:May 5, 2023, noon',body)
        self.assertIn('Quantity: 2',body)
        self.assertIn('Logged Date Time:May 5, 2023, 12:04 p.m.',body)
        self.assertIn('Processed Date Time:May 5, 2023, 12:04 p.m.',body)
        ##TODO change
        self.assertIn('Logged By:BLANK',body)

        #user goes to a respondent without processed data and sees a form!

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7001/blood_spots/')

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Collected date time:',form)

        #user submited processed form and sees processed data

        outcome_fk = Select(self.browser.find_element(By.ID, 'id_processed_form-outcome_fk'))
        outcome_fk.select_by_visible_text('Complete')

        collected = self.browser.find_element(By.ID, 'id_processed_form-collected_date_time')
        collected.clear()
        collected.send_keys('2023-09-27 12:52:26')

        processed = self.browser.find_element(By.ID, 'id_processed_form-processed_date_time')
        processed.clear()
        processed.send_keys('2023-09-27 12:52:26')

        quantity = self.browser.find_element(By.ID, 'id_processed_form-quantity')
        quantity.clear()
        quantity.send_keys('4')

        logged = self.browser.find_element(By.ID, 'id_processed_form-logged_date_time')
        logged.clear()
        logged.send_keys('2023-09-27 12:52:26')

        #user clikcs submit and sees processed data
        submit = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/input[6]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity: 4',body)

        #user goes to P7002 to see stored form
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7002/blood_spots/')

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Stored date time:',form)

        #user submits stored form to see stored data
        outcome_fk = Select(self.browser.find_element(By.ID, "id_stored_form-outcome_fk"))
        outcome_fk.select_by_visible_text('Complete')

        stored_date_time = self.browser.find_element(By.ID, "id_stored_form-stored_date_time")
        stored_date_time.clear()
        stored_date_time.send_keys('2023-09-27 12:52:26')

        storage_location = self.browser.find_element(By.ID, "id_stored_form-storage_location")
        storage_location.clear()
        storage_location.send_keys('Hospital')

        quantity = self.browser.find_element(By.ID, 'id_stored_form-quantity')
        quantity.clear()
        quantity.send_keys('6')

        logged = self.browser.find_element(By.ID, 'id_stored_form-logged_date_time')
        logged.clear()
        logged.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="blood_spot_stored"]/form/input[6]')
        submit.click()
        time.sleep(30)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity: 6',body)


        #user goes to P7000 to see stored data
