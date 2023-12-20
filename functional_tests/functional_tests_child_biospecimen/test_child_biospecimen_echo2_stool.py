from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver,Child,ChildBiospecimen
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class ChildBioSpecimenEntryStool(FunctionalTest):

    def return_child_bio_pk(self,child_id,collection_type,age):
        child_object = Child.objects.get(charm_project_identifier=child_id)
        child_biospecimen = ChildBiospecimen.objects.get(child_fk=child_object,
                                                         collection_fk__collection_type=collection_type,
                                                         age_category_fk__age_category=age)

        return child_biospecimen.pk

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME,'body').text


    def test_user_can_choose_status_of_child_stool_information_chooses_kit_sent_shipped_wsu(self):
        # User visits the caregiver biospecimen page and sees stool
        primary_key = self.return_child_bio_pk('4100F1', 'O', 'ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')

        # user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(
            self.browser.find_element(By.ID, 'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Kit Sent')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Kit sent date:', body_text)

        kit_sent_date = self.browser.find_element(By.ID, "id_kit_sent_form-kit_sent_date")
        kit_sent_date.clear()
        kit_sent_date.send_keys('2023-09-27')

        biospecimen_id = self.browser.find_element(By.ID,'id_kit_sent_form-echo_biospecimen_id')
        biospecimen_id.send_keys('5555555')

        submit = self.browser.find_element(By.XPATH, '//*[@id="initial_information"]/form/input[2]')
        submit.click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Sept. 27, 2023', body_text)
        self.assertIn('5555555', body_text)


        # user now sees the collected form

        collected_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Collected', collected_form)

        in_person_remote = Select(self.browser.find_element(By.ID, 'id_collected_child_form-in_person_remote'))
        in_person_remote.select_by_visible_text('In Person')

        date_received = self.browser.find_element(By.ID, 'id_collected_child_form-date_received')
        date_received.clear()
        date_received.send_keys('2023-09-27')

        number_of_tubes = self.browser.find_element(By.ID, 'id_collected_child_form-number_of_tubes')
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # USer now sees the collected information

        body_text = self.webpage_text()
        self.assertIn('In Person or Remote: In Person', body_text)
        self.assertIn('number of tubes: 5', body_text.lower())
        self.assertIn('date received: sept. 27, 2023', body_text.lower())

        #User sees incentive form

        incentive_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Incentive', incentive_form)

        incentive_date = self.browser.find_element(By.ID, 'id_child_incentive_form-incentive_date')
        incentive_date.send_keys('2023-09-30')

        submit = self.browser.find_element(By.XPATH, '//*[@id="incentive_form_div"]/form/input[2]')
        submit.click()

        text = self.webpage_text()
        self.assertIn('Sept. 30, 2023', text)

        #User sees shipped choice form

        shipped_choice_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Shipped to WSU', shipped_choice_form)

        shipped_choice = Select(self.browser.find_element(By.ID, 'id_child_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_choice.select_by_visible_text('Shipped to WSU')
        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_choice_form_div"]/form/input[2]')
        submit.click()

        # User sees shipped to echo form and submits a date time
        wsu_shipped_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Shipped to WSU', wsu_shipped_form)

        shipped_date_time = self.browser.find_element(By.ID, 'id_child_shipped_to_wsu_form-shipped_date_and_time')
        shipped_date_time.clear()
        shipped_date_time.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_div"]/form/input[2]')
        submit.click()

        body_text = self.webpage_text()
        self.assertIn('Shipped to WSU Date: Sept. 27, 2023',body_text)

        #User sees received at WSU form
        received_at_wsu = self.browser.find_element(By.ID, 'id_child_received_at_wsu_form-received_date_time')
        received_at_wsu.clear()
        received_at_wsu.send_keys('2023-10-04 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="received_at_wsu_div"]/form/input[2]')
        submit.click()
        body_text = self.webpage_text()
        self.assertIn('Received at WSU Date: Oct. 4, 2023',body_text)


    def test_user_can_choose_status_of_stool_information_chooses_kit_sent_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees stool
        primary_key = self.return_child_bio_pk('4100F1', 'O', 'ZF')
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

        biospecimen_id = self.browser.find_element(By.ID,'id_kit_sent_form-echo_biospecimen_id')
        biospecimen_id.send_keys('5555555')

        submit = self.browser.find_element(By.XPATH,'//*[@id="initial_information"]/form/input[2]')
        submit.click()

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Sept. 27, 2023',body_text)
        self.assertIn('5555555', body_text)

        #user now sees the collected form

        collected_form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected',collected_form)

        in_person_remote = Select(self.browser.find_element(By.ID,'id_collected_child_form-in_person_remote'))
        in_person_remote.select_by_visible_text('In Person')

        date_received = self.browser.find_element(By.ID,'id_collected_child_form-date_received')
        date_received.clear()
        date_received.send_keys('2023-09-27')

        number_of_tubes = self.browser.find_element(By.ID,'id_collected_child_form-number_of_tubes')
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #User now sees the collected information

        body_text = self.webpage_text()
        self.assertIn('In Person or Remote: In Person',body_text)

        #User sees incentive form

        incentive_form = self.browser.find_element(By.TAG_NAME, 'form').text
        self.assertIn('Incentive', incentive_form)

        incentive_date = self.browser.find_element(By.ID, 'id_child_incentive_form-incentive_date')
        incentive_date.send_keys('2023-09-30')

        submit = self.browser.find_element(By.XPATH, '//*[@id="incentive_form_div"]/form/input[2]')
        submit.click()

        shipped_choice_form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped to WSU',shipped_choice_form)

        shipped_choice = Select(self.browser.find_element(By.ID,'id_child_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_choice.select_by_visible_text('Shipped to Echo')
        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_choice_form_div"]/form/input[2]')
        submit.click()

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


    def test_user_can_choose_status_of_stool_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees stool
        primary_key = self.return_child_bio_pk('4100F1', 'O', 'ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')
        #user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')

        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)


    def test_user_can_choose_status_of_stool_information_chooses_no_consent(self):
        # User visits the caregiver biospecimen page and sees stool
        primary_key = self.return_child_bio_pk('4100F1', 'O', 'ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/child/4100F1/{primary_key}/initial/')
        #user sees initial form and submits collected
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('ID: 4100F1', body_text)
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_bio_form-collected_not_collected_kit_sent'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')

        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)