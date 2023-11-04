import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class MotherIdPageTest(FunctionalTest):
    def test_user_can_view_web_page_of_mother_ids(self):
        #User visits the initial page and is given a list of mother ids

        self.browser.get(self.live_server_url)
        self.assertIn('Charm Sample Tracking', self.browser.title)

        #User sees a list of mother ids
        link_text = self.browser.find_element(By.LINK_TEXT,'Mother Sample').text
        self.assertIn('Mother Sample', link_text)

        #User finds mother sample and clicks link
        self.browser.find_element(By.LINK_TEXT,'Mother Sample').click()
        #User types in link to caregiver page
        #self.browser.get(f'{self.browser.current_url}data/caregiver')

        #User looks for one caregiver id in page
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('P7000',body_text)
        #User sees the other charm project sampleid
        self.assertIn('P7001',body_text)

        # self.wait_for(lambda: self.assertTrue(
        #     self.browser.find_element(By.ID,''.is_displayed()
        # ))

        self.assertIn('Information Page',body_text)
        self.assertIn('Biospecimen',body_text)

        self.assertIn('Surveys',body_text)
        self.assertIn('Consent Items',body_text)

        #User clicks on Information Page link and sees mother info page
        self.browser.find_element(By.LINK_TEXT,'Information Page').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Mother\'s name is: Doe, Jane',header_text_id_page)

        self.browser.back()

        #User clicks on Biospecimen and sees mother biospecimen
        self.browser.find_element(By.LINK_TEXT,'Biospecimen').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Charm ID: P7000',header_text_id_page)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Urine',body)

        self.browser.back()

        #User clicks on Survey and sees mother surveys
        self.browser.find_element(By.LINK_TEXT,'Surveys').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Charm ID: P7000',header_text_id_page)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Prenatal 1',body)

        self.browser.back()

        #User clicks on consent and sees consent
        self.browser.find_element(By.LINK_TEXT,'Consent Items').click()
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Charm ID: P7000',header_text_id_page)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Mother Placenta',body)