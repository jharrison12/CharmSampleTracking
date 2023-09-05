from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time
import datetime
from selenium.webdriver.support.ui import Select

class MotherConsentItemPageTest(FunctionalTest):

    def test_user_can_see_consent_items(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/consentitem/')
        time.sleep(10)
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Mother Placenta', body_text)