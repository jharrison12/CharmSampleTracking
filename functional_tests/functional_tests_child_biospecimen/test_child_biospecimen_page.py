import time
import unittest

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
@unittest.skip
class ChildBiospecimenPageTest(FunctionalTest):

    def test_user_can_see_child_page(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/biospecimen/')
        header = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('Child ID: 7000M1',header)

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Toenail',body)
        self.assertIn('Urine',body)
        self.assertIn('Hair',body)
