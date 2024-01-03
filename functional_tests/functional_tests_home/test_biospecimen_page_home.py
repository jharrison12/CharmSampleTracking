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

        #user looks for 4100 and clicks on the link
        body = self.webpage_text()
        self.assertIn('Charm ID',body)
        self.assertIn('4100',body)
        self.assertIn('4702', body)

        search_bar = self.browser.find_element(By.ID,"myInput")
        search_bar.clear()
        search_bar.send_keys('4100')

        body = self.webpage_text()

        #test that your javascript works that hides ids
        self.assertNotIn('4702',body)

        self.browser.find_element(By.LINK_TEXT, '4100').click()

        #user sees a list or biospecimen for 4100
        #user also sees trimesters listed

        body = self.webpage_text()
        self.assertIn('Trimester 2',body)
        self.assertIn('Blood 4100 (12BL4100)',body)

