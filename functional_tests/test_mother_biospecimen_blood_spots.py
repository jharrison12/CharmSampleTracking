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
        time.sleep(60)

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

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity: 6',body)

        #user now sees shipped form

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Shipped date time:', form)
        self.assertIn('Outcome fk:', form)
        self.assertIn('Shipping number:', form)

        #user submits shipped form
        # user submits stored form to see stored data
        outcome_fk = Select(self.browser.find_element(By.ID, "id_shipped_form-outcome_fk"))
        outcome_fk.select_by_visible_text('Complete')

        stored_date_time = self.browser.find_element(By.ID, "id_shipped_form-shipped_date_time")
        stored_date_time.clear()
        stored_date_time.send_keys('2023-09-27 12:52:26')

        shipping_number = self.browser.find_element(By.ID, "id_shipped_form-shipping_number")
        shipping_number.clear()
        shipping_number.send_keys('7775557')

        quantity = self.browser.find_element(By.ID, 'id_shipped_form-quantity')
        quantity.clear()
        quantity.send_keys('12')

        logged = self.browser.find_element(By.ID, 'id_shipped_form-logged_date_time')
        logged.clear()
        logged.send_keys('2023-09-27 12:52:26')

        courier = self.browser.find_element(By.ID, 'id_shipped_form-courier')
        courier.clear()
        courier.send_keys('Fedex')

        submit = self.browser.find_element(By.XPATH, '//*[@id="blood_spot_shipped"]/form/input[7]')
        submit.click()

        #user sees shipped data just submitted.

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity: 12',body)
        self.assertIn('Shipping Number:7775557',body)
        self.assertIn('Courier:Fedex',body)

        #user now sees received form

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Received date time:', form)
        self.assertIn('Outcome fk:', form)
        self.assertIn('Quantity:', form)
        self.assertIn('Storage location:', form)

        #user submits received form and now sees received data
        # user submits stored form to see stored data

        outcome_fk = Select(self.browser.find_element(By.ID, "id_received_form-outcome_fk"))
        outcome_fk.select_by_visible_text('Complete')

        received_date_time = self.browser.find_element(By.ID, "id_received_form-received_date_time")
        received_date_time.clear()
        received_date_time.send_keys('2023-09-27 12:52:26')

        quantity = self.browser.find_element(By.ID, 'id_received_form-quantity')
        quantity.clear()
        quantity.send_keys('19')

        logged = self.browser.find_element(By.ID, 'id_received_form-logged_date_time')
        logged.clear()
        logged.send_keys('2023-09-27 12:52:26')

        storage_location_received = self.browser.find_element(By.ID, 'id_received_form-storage_location')
        storage_location_received.clear()
        storage_location_received.send_keys('MSU')

        submit = self.browser.find_element(By.XPATH, '//*[@id="blood_spot_information"]/form/input[6]')
        self.browser.execute_script("arguments[0].scrollIntoView();", submit)
        self.browser.execute_script("arguments[0].click();", submit)



        #user goes to P7000 to see stored data
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity:19',body)
        self.assertIn('Storage Location:MSU',body)

