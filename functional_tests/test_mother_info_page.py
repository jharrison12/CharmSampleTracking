from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class MotherInformationPageTest(FunctionalTest):

    def test_user_can_see_mother_information_page(self):

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000')
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Mothers name is: Doe, Jane',header_text_id_page)
        #time.sleep(30)
        body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('July 3, 1985',body_text_id_page)
        self.assertIn('P7000',body_text_id_page)
        self.assertIn('0000',body_text_id_page)
        self.assertIn('01',body_text_id_page)
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
