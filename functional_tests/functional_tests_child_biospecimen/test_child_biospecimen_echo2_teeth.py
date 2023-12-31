from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver,Child,ChildBiospecimen
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class ChildBioSpecimenEntryTooth(FunctionalTest):

    def return_child_bio_pk(self,child_id,collection_type,age,collection_number):
        child_object = Child.objects.get(charm_project_identifier=child_id)
        child_biospecimen = ChildBiospecimen.objects.get(child_fk=child_object,
                                                         collection_fk__collection_type=collection_type,
                                                         age_category_fk__age_category=age,
                                                         collection_fk__collection_number=collection_number)

        return child_biospecimen.pk

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME,'body').text


    def test_user_can_choose_status_of_tooth_twelve_to_thirteen_months_chooses_kit_sent_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees blood_spots
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST',collection_number=1)
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')

        #user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Kit Sent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Kit sent date:', body_text)

        kit_sent_date = self.browser.find_element(By.ID,"id_kit_sent_form-kit_sent_date")
        kit_sent_date.clear()
        kit_sent_date.send_keys('2023-09-27')

        biospecimen_id = self.browser.find_element(By.ID, 'id_kit_sent_form-echo_biospecimen_id')
        biospecimen_id.send_keys('5555555')

        submit = self.browser.find_element(By.XPATH, '//*[@id="initial_information"]/form/input[2]')
        submit.click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Sept. 27, 2023',body_text)

        #user now sees the collected form

        collected_form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected',collected_form)
        self.assertNotIn('number of cards',collected_form.lower())
        self.assertNotIn('in person remote',collected_form.lower())


        date_collected = self.browser.find_element(By.ID,'id_collected_child_form-date_collected')
        date_collected.clear()
        date_collected.send_keys('2023-09-27')

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees incentive form
        incentive_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Incentive', incentive_form)

        incentive_date = self.browser.find_element(By.ID, 'id_child_incentive_form-incentive_date')
        incentive_date.send_keys('2023-09-30')

        submit = self.browser.find_element(By.XPATH, '//*[@id="incentive_form_div"]/form/input[2]')
        submit.click()

        text = self.webpage_text()
        self.assertIn('Sept. 30, 2023', text)

        #User sees shipped to echo form and submits a date time
        echo_shipped_form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped to Echo',echo_shipped_form)

        echo_shipped_date = self.browser.find_element(By.ID, 'id_child_shipped_to_echo_form-shipped_date_and_time')
        echo_shipped_date.clear()
        echo_shipped_date.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_echo_div"]/form/input[2]')
        submit.click()

        body_text = self.webpage_text()
        self.assertIn('Shipped to Echo Date: Sept. 27, 2023',body_text)

    def test_user_can_choose_status_of_teeth_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees blood_spots
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST',collection_number=1)
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')
        #user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form',body_text)

        self.assertNotIn('No Consent',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')

        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)


    def test_user_can_choose_status_of_teeth_information_chooses_declined(self):
        # User visits the caregiver biospecimen page and sees blood_spots
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST',collection_number=1)
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')
        #user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form',body_text)

        self.assertNotIn('No Consent',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Declined')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')

        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Declined', body_text)

        declined_date = self.browser.find_element(By.ID,'id_declined_form-declined_date')
        declined_date.clear()
        declined_date.send_keys('2023-09-28')
        submit = self.browser.find_element(By.XPATH,'//*[@id="declined_information"]/form/input[2]')

        submit.click()

        body_text = self.webpage_text()
        self.assertIn('Sept. 28, 2023',body_text)
