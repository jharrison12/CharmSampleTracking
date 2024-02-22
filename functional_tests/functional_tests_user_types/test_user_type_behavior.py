import logging

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest, TODAY
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class UserTypeBehaviorTest(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def webpage_text(self):
        return self.browser.find_element(By.TAG_NAME, 'body').text

    def test_user_visits_home_page_and_only_sees_charm_ids_for_their_recruitment(self):
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}')

        body = self.webpage_text()
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text

        self.browser.get(f'{self.browser.current_url}biospecimen/charm_ids/')

        # user looks for 4100 and clicks on the link
        body = self.webpage_text()
        self.assertIn('Charm ID', body)
        self.assertIn('4100', body)
        self.assertNotIn('4400', body)
        self.assertNotIn('470000', body)

        search_bar = self.browser.find_element(By.ID, "myInput")
        search_bar.clear()
        search_bar.send_keys('4100')