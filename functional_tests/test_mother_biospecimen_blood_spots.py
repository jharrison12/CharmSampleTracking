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
        self.assertIn("Log Status: Completed", body)

        #User sees processed information if there is processed data
        self.assertIn(body,'ID: 1111BS')
        self.assertIn(body,'Collected Date Time:May 5, 2023, noon')
        self.assertIn(body,'Quantity: 2')
        self.assertIn(body,'Logged Date Time:May 5, 2023, 12:04 p.m.')
        self.assertIn(body,'Processed Date Time:May 5, 2023, 12:04 p.m.')
        ##TODO change
        self.assertIn(body,'Logged By:BLANK')

        #user goes to a respondent without processed ata and sees a form!

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7001/blood_spots/')
