from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time

class MotherBioSpecimenPageTest(FunctionalTest):

    def test_user_can_see_bio_specimen_information(self):
        # User visits the caregiver biospecimen page and sees urine
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/biospecimen')

        header_text = self.browser.find_elements(By.TAG_NAME,'h2')
        self.assertIn('ID',[item.text for item in header_text])
        mother_id_section = self.browser.find_element(By.CLASS_NAME,'mother_id').text
        time.sleep(10)
        self.assertIn('P7000',mother_id_section)
        self.assertIn('4444',mother_id_section)

        serum_section = self.browser.find_element(By.CLASS_NAME,'mother_serum').text
        self.assertIn("Serum 1: Completed", serum_section)
        self.assertIn("Serum 2: Incomplete", serum_section)

        plasma_section = self.browser.find_element(By.CLASS_NAME,'mother_plasma').text
        self.assertIn("Plasma 1: Completed", plasma_section)
        self.assertIn("Plasma 2: Incomplete", plasma_section)

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Urine 1: Completed',body_text)
        self.assertIn('Urine 2: Incomplete',body_text)

        #user visits anoter sampleid to view urine outcome

        self.browser.get(f'{self.browser.current_url}data/caregiver/P7001/biospecimen')
        self.assertIn('Urine 1: Completed', body_text)