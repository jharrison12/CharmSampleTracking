import logging
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Collected,PregnancyTrimester,ShippedWSU,ShippedECHO,KitSent,AgeCategory,\
    User,Caregiver,Incentive,Project,\
    Child,Pregnancy
import datetime,pytz
from selenium.webdriver.common.by import By
import time
from django.utils import timezone
import os

logging.basicConfig(level=logging.CRITICAL)

class FunctionalTest(StaticLiveServerTestCase):
    fixtures = ['initialdata']

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            return

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}/accounts/login/')
        username = self.browser.find_element(By.ID,'id_username')
        username.send_keys('testuser')
        password = self.browser.find_element(By.ID,'id_password')
        password.send_keys('secret')
        login = self.browser.find_element(By.ID,'login_button')
        login.click()


    def tearDown(self):
        self.browser.quit()


def wait_for_element(browser,myelement):
    #logging.debug(browser,myelement)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, myelement))
        )
    except:
        raise AssertionError

    return element