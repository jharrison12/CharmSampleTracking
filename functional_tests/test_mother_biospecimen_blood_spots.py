from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time
import datetime
from selenium.webdriver.support.ui import Select

class MotherBioSpecimenBloodspotsTest(FunctionalTest):

    def test_user_can_see_bio_blood_spot_information(self):
        # User visits the caregiver biospecimen page and sees urine
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/blood_spots/')
        time.sleep(20)
        header_text = self.browser.find_elements(By.TAG_NAME,'h1')
        self.assertIn('Charm ID: P7000 Family ID: 4444',[item.text for item in header_text])

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn("ID: 1111BS", body)
