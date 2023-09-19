import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class MotherInformationPageTest(FunctionalTest):

    def test_user_can_see_mother_information_page(self):

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000')
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Mother\'s name is: Doe, Jane',header_text_id_page)

        body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('July 3, 1985',body_text_id_page)
        self.assertIn('P7000',body_text_id_page)
        self.assertIn('0000',body_text_id_page)
        self.assertIn('01',body_text_id_page)
        self.assertIn('White',body_text_id_page)
        self.assertIn('Non-Hispanic',body_text_id_page)
        self.assertIn('Echo Pin: 333',body_text_id_page)
        self.assertIn('Specimen Id: 4444',body_text_id_page)
        self.assertIn('Address: One Drive', body_text_id_page)
        self.assertIn('Lansing', body_text_id_page)
        self.assertIn('MI', body_text_id_page)
        self.assertIn('38000', body_text_id_page)
        self.assertIn('Email Primary: jharrison12@gmail.com', body_text_id_page)
        self.assertIn('Email Secondary: f@gmail.com', body_text_id_page)
        self.assertIn('Primary Phone: 555-555-5555', body_text_id_page)
        self.assertIn('Secondary Phone: 666-666-6666', body_text_id_page)
        self.assertIn('Twitter: @jonathan', body_text_id_page)
        self.assertIn('Facebook: jonathan-h', body_text_id_page)
        self.assertIn('Instagram: @jonathanscat', body_text_id_page)

        #User visits the page for P7001
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7001')
        body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('P7001', body_text_id_page)

    def test_user_can_view_personal_contact_information(self):
        #User visits caregiver contact page
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/')
        contact_body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Contact A First Name: John', contact_body_text_id_page)
        self.assertIn('Contact A Last Name: Jones', contact_body_text_id_page)
        self.assertIn('Contact A Phone Number: 999-999-9999', contact_body_text_id_page)
        self.assertIn('Contact A Address: two drive', contact_body_text_id_page)
        self.assertIn('Contact A Email: b@b.com', contact_body_text_id_page)

        #User can also see Contact B if contact b exists
        self.assertIn('Contact B First Name: Jessica', contact_body_text_id_page)
        self.assertIn('Contact B Last Name: Jones', contact_body_text_id_page)
        self.assertIn('Contact B Phone Number: 999-999-9998',contact_body_text_id_page)
        self.assertIn('Contact B Address: two drive',contact_body_text_id_page)
        self.assertIn('Contact B Email: c@c.com', contact_body_text_id_page)

        #User visits a different caregivers page which has no contact B
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7001/')
        contact_body_text_id_page_70001 = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Contact A First Name: James', contact_body_text_id_page_70001)
        self.assertIn('Contact A Last Name: Contact', contact_body_text_id_page_70001)
        self.assertIn('Contact A Phone Number: 999-999-9997', contact_body_text_id_page_70001)
        self.assertIn('Contact A Address: three drive', contact_body_text_id_page_70001)
        self.assertIn('Contact A Email: d@d.com', contact_body_text_id_page_70001)
        self.assertNotIn('Contact B',contact_body_text_id_page_70001)

    @unittest.skip
    def test_user_can_visit_caregiver_survey_page(self):
        #i cannot get selenium to find the link.
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/')
        self.browser.implicitly_wait(5)

        link = self.browser.find_element(By.XPATH,'//*[@id="survey_link"]')
        self.browser.implicitly_wait(5)
        # webdriver.ActionChains(self.browser).move_to_element(link).click(link).perform()
        link.click()

        surveys = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn("Prenatal 1:", surveys)
        self.assertIn("Prenatal 2:", surveys)

