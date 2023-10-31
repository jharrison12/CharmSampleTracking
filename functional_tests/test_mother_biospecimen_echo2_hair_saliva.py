from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class MotherBioSpecimenEcho2EntryTestUrine(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester,child_age=None):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        age_category_fk__age_category=child_age)
        return caregiverbio.pk


    def test_user_can_choose_status_of_hair_or_saliva_information_chooses_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)


        #user submits form and sees data

        in_person_remote = Select(self.browser.find_element(By.ID, 'id_hair_saliva_form-in_person_remote'))
        in_person_remote.select_by_visible_text('In Person')

        collected = self.browser.find_element(By.ID,"id_hair_saliva_form-date_collected")
        collected.clear()
        collected.send_keys('2023-09-27')

        incentive_date = self.browser.find_element(By.ID,"id_hair_saliva_form-incentive_date")
        incentive_date.clear()
        incentive_date.send_keys('2023-09-27')

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Collected Date Time: Sept. 27, 2023', body)

        #user sees option to choose shipped to wsu or shipped to echo

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped Choice Form',form)

        self.assertNotIn('Shipped to WSU',form)
        shipped_to_echo = Select(self.browser.find_element(By.ID,'id_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_to_echo.select_by_visible_text('Shipped to Echo')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_choice"]/form/input[2]')

        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        needed_div = self.browser.find_element(By.ID,'shipped_to_echo_form').text

        self.assertIn('Shipped to ECHO Form',needed_div)

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_echo_form-shipped_date_and_time")
        shipped_date_time.clear()
        shipped_date_time.send_keys('2023-10-20 09:17:07')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_echo_form"]/form/input[2]')

        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped Date Time: Oct. 20, 2023, 9:17 a.m.',body)

    def test_user_can_choose_status_of_hair_or_salvia_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('Not Collected', body_text)

    def test_user_can_choose_status_of_hair_or_salvia_information_chooses_no_consent(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, child_age='ZF')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('No Consent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('No Consent', body_text)