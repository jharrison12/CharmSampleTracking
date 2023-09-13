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

        #User clicks on Information Page link and sees child info page
        self.browser.find_element(By.LINK_TEXT,'Information Page').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text

        self.assertIn('Child\'s name is: Harrison, Jonathan',header_text_id_page)

        self.browser.back()

        self.assertIn('Survey Page',body_text)
        #user clicks on Survey Page and sees child survey page
        self.browser.find_element(By.LINK_TEXT, 'Survey Page').click()
        header_text_survey_page = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn("Child ID: 7000M1",header_text_survey_page)
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Eight Year Survey: Completed',body_text)
        self.assertIn('Eight Year Survey Date: Sept. 12, 2023',body_text)

        self.browser.back()

        self.assertIn('Assent Page',body_text)

        # self.assertIn('Biospecimen',body_text)



