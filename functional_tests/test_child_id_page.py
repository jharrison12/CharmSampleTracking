import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ChildIdPageTest(FunctionalTest):

    def test_user_can_see_child_id(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Charm Sample Tracking', self.browser.title)
        #User sees a child sample link
        link_text = self.browser.find_element(By.LINK_TEXT,'Child Sample').text
        self.assertIn('Child Sample', link_text)

        self.browser.find_element(By.LINK_TEXT,'Child Sample').click()
        #User looks for one child id in page
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('7000M1',body_text)
        self.assertIn('Information Page',body_text)
        self.assertIn('Biospecimen',body_text)

        self.assertIn('Surveys',body_text)
        self.assertIn('Consent Items',body_text)

        #User clicks on Information Page link and sees mother info page
        self.browser.find_element(By.LINK_TEXT,'Information Page').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Child\'s name is: Doe, Jane',header_text_id_page)

        self.browser.back()
