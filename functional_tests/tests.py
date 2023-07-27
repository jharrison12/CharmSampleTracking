from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from dataview.models import Caregiver
import time

MAX_WAIT =10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        Caregiver.objects.create(charm_project_identifier='P7000')
        Caregiver.objects.create(charm_project_identifier='P7001')

    def tearDown(self):
        self.browser.quit()


    def test_user_can_view_web_page_of_mother_ids(self):
        #User visits the initial page and is given a list of mother ids
        self.browser.get(self.live_server_url)
        self.assertIn('Charm Sample Tracking', self.browser.title)

        #User sees a list of mother ids
        link_text = self.browser.find_element(By.LINK_TEXT,'Mother Sample').text
        self.assertIn('Mother Sample', link_text)

        #User types in link to caregiver page
        self.browser.get(f'{self.browser.current_url}data/caregiver')
        time.sleep(10)
        #User looks for one caregiver id in page
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('P7000',body_text)
        #User sees the other charm project sampleid
        self.assertIn('P7001',body_text)
