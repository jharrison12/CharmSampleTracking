import logging
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
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
            self.browser.get(self.live_server_url)
            self.browser.get(f'{self.browser.current_url}/accounts/login/')
            username = self.browser.find_element(By.ID, 'id_username')
            username.send_keys('testuser')
            password = self.browser.find_element(By.ID, 'id_password')
            password.send_keys('secret')
            login = self.browser.find_element(By.ID, 'login_button')
            login.click()
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

    def choose_flatpickr_day(self,number_of_css_selector):
        try:
            WebDriverWait(self.browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'span.flatpickr-day.today')))
            flatpickr_class = self.browser.find_elements(By.CSS_SELECTOR,'span.flatpickr-day.today')[number_of_css_selector]
            flatpickr_class.click()
            #find element body will click in the middle of the page and choose a different date lol
            self.browser.find_element(By.TAG_NAME,'h1').click()
            number_of_css_selector+=1
        except IndexError:
            logging.debug(
                f"number of flat picker days {len(self.browser.find_elements(By.CSS_SELECTOR, 'span.flatpickr-day.today'))}")
            logging.debug(
                f"flat picker days {self.browser.find_elements(By.CSS_SELECTOR, 'span.flatpickr-day.today')}")
        return number_of_css_selector


def wait_for_element(browser,myelement):
    #logging.debug(browser,myelement)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, myelement))
        )
    except:
        raise AssertionError

    return element

TODAY = dt.datetime.now().strftime('%B %#d, %Y')