import time
import unittest

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class Echo2BioPage(FunctionalTest):
    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def test_user_visits_home_page_and_sees_charm_ids(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}')

        body = self.webpage_text()

        #self.browser.find_element(By.PARTIAL_LINK_TEXT,'Charm').click()
        #The above doesn't work in the ft, so you have to manually go there
        self.browser.get(f'{self.browser.current_url}biospecimen/charm_ids/')
        time.sleep(50)
        #user looks for 4100 and clicks on the link
        body = self.webpage_text()
        self.assertIn('Charm ID',body)
        self.assertIn('4100',body)
        self.browser.find_element(By.LINK_TEXT, '4100').click()

        #user sees a list or biospecimen for 4100
        body = self.webpage_text()
        self.assertIn('12BL410001',body)