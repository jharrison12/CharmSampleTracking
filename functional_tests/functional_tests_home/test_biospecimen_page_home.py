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

        self.browser.find_element(By.LINK_TEXT,'Biospecimen Entry').click()


        self.assertIn('Charm ID',body)