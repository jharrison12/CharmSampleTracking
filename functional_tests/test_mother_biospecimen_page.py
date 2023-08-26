from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
import time
import datetime

class MotherBioSpecimenPageTest(FunctionalTest):

    def test_user_can_see_bio_specimen_information(self):
        # User visits the caregiver biospecimen page and sees urine
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000/biospecimen')

        header_text = self.browser.find_elements(By.TAG_NAME,'h2')
        self.assertIn('ID',[item.text for item in header_text])
        mother_id_section = self.browser.find_element(By.CLASS_NAME,'mother_id').text
        time.sleep(5)
        self.assertIn('P7000',mother_id_section)
        self.assertIn('4444',mother_id_section)

        serum_section = self.browser.find_element(By.CLASS_NAME,'mother_serum').text
        self.assertIn("Serum 1: Completed", serum_section)
        self.assertIn("Serum 2: Incomplete", serum_section)
        self.assertIn(f"Date: Aug. 23, 2023", serum_section)

        plasma_section = self.browser.find_element(By.CLASS_NAME,'mother_plasma').text
        self.assertIn("Plasma 1: Completed", plasma_section)
        self.assertIn("Plasma 2: Incomplete", plasma_section)

        bloodspots_section = self.browser.find_element(By.CLASS_NAME,'mother_bloodspots').text
        self.assertIn("Bloodspots 1: Completed", bloodspots_section)
        self.assertIn("Bloodspots 2: Incomplete", bloodspots_section)

        whole_blood_section = self.browser.find_element(By.CLASS_NAME,'mother_whole_blood').text
        self.assertIn("Whole Blood 1: Completed", whole_blood_section)
        self.assertIn("Whole Blood 2: Incomplete", whole_blood_section)

        buffy_coat_section = self.browser.find_element(By.CLASS_NAME,'mother_buffy_coat').text
        self.assertIn("Buffy Coat 1: Completed", buffy_coat_section)
        self.assertIn("Buffy Coat 2: Incomplete", buffy_coat_section)

        red_blood_cells = self.browser.find_element(By.CLASS_NAME,'mother_red_blood_cells').text
        self.assertIn("Red Blood Cells 1: Completed", red_blood_cells)
        self.assertIn("Red Blood Cells 2: Incomplete", red_blood_cells)

        urine = self.browser.find_element(By.CLASS_NAME,'mother_urine').text
        self.assertIn("Urine 1: Completed", urine)
        self.assertIn("Urine 2: Incomplete", urine)
        self.assertIn("Urine 3: Completed", urine)
        self.assertIn("Urine EC: Incomplete", urine)
        self.assertIn("Urine MC: Incomplete", urine)

        hair = self.browser.find_element(By.CLASS_NAME,'mother_hair').text
        self.assertIn("Prenatal Hair: Collected", hair)
        self.assertIn("Prenatal Hair Date: Aug. 23, 2023", hair)
        self.assertIn("Prenatal Hair GC: Aug. 24, 2023", hair)

        toenails = self.browser.find_element(By.CLASS_NAME,'mother_toenails').text
        self.assertIn("Prenatal Toenail: Collected", toenails)
        self.assertIn("Prenatal Toenail Date: Aug. 26, 2023", toenails)
        self.assertIn("Prenatal Toenail GC: Aug. 26, 2023", toenails)

        #user visits anoter sampleid to view urine outcome

        # self.browser.get(f'{self.browser.current_url}data/caregiver/P7001/biospecimen')
        # self.assertIn('Urine 1: Completed', body_text)