import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ChildInformationPageTest(FunctionalTest):

    def test_user_can_see_child_page(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/')

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('7000M1',body)
        self.assertIn('White',body)
        self.assertIn('Hispanic',body)
        self.assertIn('May 20, 2023',body)
        self.assertIn('Male',body)
        self.assertIn('University of Michigan',body)
        self.assertIn('Is twin?: False',body)

        #user sees caregiver information
        self.assertIn('Caregiver\'s Charm ID: P7000',body)
        self.assertIn('Is biological mother?: True',body)
        # User make sure that 7002M1's pcg is not mother
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7001M1/')
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Is biological mother?: False',body)
        self.assertIn('Relation: Mother-in-law',body)


        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/')
        mothers_link = self.browser.find_element(By.LINK_TEXT,"P7000")
        mothers_link.click()

        header = self.browser.find_element(By.TAG_NAME,"h1").text
        self.assertIn("Mother's name is: Doe, Jane",header)

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/')

        body = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertIn('One Drive',body)
        self.assertIn('Gestational Age at Birth: 2',body)