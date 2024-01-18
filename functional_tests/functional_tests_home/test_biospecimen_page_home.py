from selenium.webdriver.support.ui import Select
import time
import unittest

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest

class Echo2BioPage(FunctionalTest):
    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def user_clicks_into_blood_4100(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}')

        body = self.webpage_text()

        # self.browser.find_element(By.PARTIAL_LINK_TEXT,'Charm').click()
        # The above doesn't work in the ft, so you have to manually go there
        self.browser.get(f'{self.browser.current_url}biospecimen/charm_ids/')

        # user looks for 4100 and clicks on the link
        body = self.webpage_text()
        self.assertIn('Charm ID', body)
        self.assertIn('4100', body)
        self.assertIn('4702', body)

        search_bar = self.browser.find_element(By.ID, "myInput")
        search_bar.clear()
        search_bar.send_keys('4100')

        body = self.webpage_text()

        # test that your javascript works that hides ids
        self.assertNotIn('4702', body)

        self.browser.find_element(By.ID, '4100_button').click()
        ##TODO remove this sleep.  Currently needed for modal to appear.
        time.sleep(1)
        # User sees modal asking for confirmation of bio id
        self.browser.find_element(By.LINK_TEXT, 'Confirm').click()

        # user sees a list or biospecimen for 4100
        # user also sees trimesters listed
        body = self.webpage_text()
        time.sleep(1)
        self.assertIn('Trimester 2', body)
        trimester_2_list = self.browser.find_element(By.ID, 'trimester_2_list').text

        self.assertIn('Blood 4100 (12BL410001)', trimester_2_list)

        trimester_3_list = self.browser.find_element(By.ID, 'trimester_3_list').text
        self.assertIn('Blood 4100 (13BL410001)', trimester_3_list)

        perinatal_list = self.browser.find_element(By.ID, 'perinatal_list').text

        self.assertIn('Placenta 4100 (12PL410001)', perinatal_list)

        postnatal_list = self.browser.find_element(By.ID, 'postnatal_list').text

        self.assertIn('Hair 4100 (12HA410001)', postnatal_list)

        # click on blood enter some data

        self.browser.find_element(By.LINK_TEXT, 'Blood 4100 (12BL410001)').click()
        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text


    def test_user_visits_home_page_and_sees_charm_ids(self):
        self.user_clicks_into_blood_4100()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Collected Form', form)

        # user submits form and sees data
        collected = self.browser.find_element(By.ID, "id_blood_form-collected_date_time")
        collected.click()
        number_of_element = self.choose_flatpickr_day(0)

        processed = self.browser.find_element(By.ID, "id_blood_form-processed_date_time")
        processed.click()
        number_of_element1=self.choose_flatpickr_day(number_of_element)

        stored = self.browser.find_element(By.ID, "id_blood_form-stored_date_time")
        stored.click()
        self.choose_flatpickr_day(number_of_element1)


        # user sees a ton of checkboxes for all the bloods possible
        # user does not see whole blood number of tubes until whole blood is checked

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertNotIn('Number of Tubes:', body)
        self.assertIn('Plasma', body)
        self.assertIn('Whole Blood', body)
        self.assertIn('Serum', body)
        self.assertIn('Red Blood Cells', body)
        self.assertIn('Buffy Coat', body)

        whole_blood_checkbox = self.browser.find_element(By.ID, "id_blood_form-whole_blood")
        whole_blood_checkbox.click()

        whole_blood_tubes = self.browser.find_element(By.ID, "id_blood_form-whole_blood_number_of_tubes")
        whole_blood_tubes.send_keys(3)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()
        #return to home page
        self.user_clicks_into_blood_4100()

        # go back to specimen and see incentive form is still there

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Incentive Form',form)

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.click()
        self.choose_flatpickr_day(0)