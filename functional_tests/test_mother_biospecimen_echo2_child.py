from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class ChildBioSpecimenEntry(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def test_user_can_choose_status_of_child_urine_information_chooses_kit_sent_shipped_wsu(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')


    def test_user_can_choose_status_of_urine_information_chooses_kit_sent_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')


    def test_user_can_choose_status_of_urine_information_chooses_kit_sent_not_collected(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
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

    def test_user_can_choose_status_of_urine_information_chooses_kit_sent_no_consent(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
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