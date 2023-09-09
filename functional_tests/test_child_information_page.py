import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ChildInformationPageTest(FunctionalTest):

    def test_user_can_see_child_page(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/')
        time.sleep(60)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Caregiver\'s Charm ID: P7000',body)
        self.assertIn('7000M1',body)
        self.assertIn('July 3, 2020',body)
        self.assertIn('Male',body)
        self.assertIn('University of Michigan',body)
        self.assertIn('Is twin?: False',body)
