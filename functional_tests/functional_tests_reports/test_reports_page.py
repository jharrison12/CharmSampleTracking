import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class ReportsPageTest(FunctionalTest):

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def test_user_can_see_reports_page_visits_caregiver_report(self):
        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.get(f'{self.browser.current_url}caregiver_report/')

        text = self.webpage_text()
        time.sleep(50)
        self.assertIn('4100',text)
        self.assertIn('4101',text)



    def test_user_can_see_biospecimen_report(self):
        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports',text)
        self.browser.get(f'{self.browser.current_url}biospecimen_report/')

        text = self.webpage_text()

        self.assertIn('4100',text)

    def test_user_can_see_incentive_list(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.get(f'{self.browser.current_url}incentive_/')

        text = self.webpage_text()

        self.assertIn('4100', text)


    def test_user_can_see_no_specimen_report(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}reports/')

        text = self.webpage_text()

        self.assertIn('Reports', text)
        self.browser.get(f'{self.browser.current_url}no_specimen_report/')

        text = self.webpage_text()
        time.sleep(50)
        self.assertIn('4100', text)

