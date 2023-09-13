import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ChildInformationPageTest(FunctionalTest):

    def test_user_can_see_child_page(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/assent/')
        header = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('Child ID: 7000M1',header)
        time.sleep(30)
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Eight Year Survey: True',body)
