import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ReportsPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def test_user_can_see_incentive_list(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}lists/')

        text = self.webpage_text()

        self.assertIn('Incentive', text)
        self.browser.get(f'{self.browser.current_url}incentive_list/caregiver/')

        text = self.webpage_text()

        self.assertIn('P7000', text)
        self.assertIn('Hair', text)


