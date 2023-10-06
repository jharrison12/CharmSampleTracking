import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ChildSurveyPageTest(FunctionalTest):

    def test_user_can_see_child_survey_page(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/child/7000M1/survey/')

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Eight Year Survey: Completed',body)
        self.assertIn('Eight Year Survey Date: May 3, 2023',body)

        self.assertNotIn('Incentive',body)
