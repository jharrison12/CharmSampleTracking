from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time

class CaregiverSurveyPageTest(FunctionalTest):

    def test_user_can_see_caregivers_survey_information(self):
        #User visits the caregiver survey page
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/survey')

        #User sees information on Prenatal 1 Survey for P7000
        survey_body_text_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Prenatal 1: Complete',survey_body_text_page)
        self.assertIn('Prenatal 2: Incomplete',survey_body_text_page)