from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time

class MotherPersonalContactPageTest(FunctionalTest):

    def test_user_can_view_personal_contact_information(self):
        #User visits caregiver contact page
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/contact')
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
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7001/contact')
        contact_body_text_id_page_70001 = self.browser.find_element(By.TAG_NAME,'body').text
        time.sleep(30)
        self.assertIn('Contact A First Name: James', contact_body_text_id_page_70001)
        self.assertIn('Contact A Last Name: Contact', contact_body_text_id_page_70001)
        self.assertIn('Contact A Phone Number: 999-999-9997', contact_body_text_id_page_70001)
        self.assertIn('Contact A Address: three drive', contact_body_text_id_page_70001)
        self.assertIn('Contact A Email: d@d.com', contact_body_text_id_page_70001)
        self.assertNotIn('Contact B',contact_body_text_id_page_70001)






