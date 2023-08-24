from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time

class MotherBioSpecimenPageTest(FunctionalTest):

    def test_user_can_see_bio_specimen_information(self):
        # User visits the caregiver biospecimen page and sees urine
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/biospecimen')
        time.sleep(20)
        header_text = self.browser.find_element(By.TAG_NAME,'h2').text
        self.assertIn('Specimen Id: 4444',header_text)
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Urine 1: Completed',body_text)
