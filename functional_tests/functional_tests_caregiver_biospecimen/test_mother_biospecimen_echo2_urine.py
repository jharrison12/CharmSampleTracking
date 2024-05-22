import logging

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest, TODAY
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class MotherBioSpecimenEcho2EntryTestUrine(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        logging.debug(f"{mother_one}")
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester)
        return caregiverbio.pk

    def user_submits_urine_collected(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4101', 'U', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/initial/')

        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4101', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page

        form = self.browser.find_element(By.ID, 'collected_information_form').text
        self.assertIn('Collected Form', form)

        # user submits form and sees data

        food_eat_time = self.browser.find_element(By.ID, "id_urine_form-eat_drink_datetime")
        food_eat_time.click()
        self.choose_flatpickr_day(0)

        food_eat_list = self.browser.find_element(By.ID, "id_urine_form-eat_drink_text_field")
        food_eat_list.send_keys('Bread')

        collected = self.browser.find_element(By.ID, "id_urine_form-collected_date_time")
        collected.click()
        time.sleep(2)
        self.choose_flatpickr_day(1)

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

    def user_submits_urine_processed(self):

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Collection Location: Clinic',body)

        aliquoted_off_site = self.browser.find_element(By.ID, "id_processed_form-processed_aliquoted_off_site")
        aliquoted_off_site.send_keys('Refrigerated')

        aliquoted_date_time = self.browser.find_element(By.ID, "id_processed_form-processed_aliquoted_date_time")
        aliquoted_date_time.click()
        self.choose_flatpickr_day(0)

        #id_processed_form-total_volume_of_urine_in_collection_cup
        total_volume_of_urine = self.browser.find_element(By.ID, "id_processed_form-total_volume_of_urine_in_collection_cup")
        total_volume_of_urine.send_keys(100)
        #processed_form-processed_aliquoted_off_site

        precipate_at_bottom = self.browser.find_element(By.ID,'id_processed_form-precipate_bottom_of_container')
        precipate_at_bottom.click()

        placed_in_fridge = self.browser.find_element(By.ID,'id_processed_form-refrigerated_prior_to_processing')
        placed_in_fridge.click()

        refrigerated_date_time = self.browser.find_element(By.ID, "id_processed_form-refrigerated_placed_date_time")
        refrigerated_date_time.click()
        self.choose_flatpickr_day(1)

        refrigerated_removed_date_time = self.browser.find_element(By.ID, "id_processed_form-refrigerated_removed_date_time")
        refrigerated_removed_date_time.click()
        self.choose_flatpickr_day(2)

        all_18_collected = Select(
            self.browser.find_element(By.ID, 'id_processed_form-all_18_collected'))
        all_18_collected.select_by_visible_text('No')

        partial_aliquot_18ml_volume = self.browser.find_element(By.ID,'id_processed_form-partial_aliquot_18ml_volume')
        partial_aliquot_18ml_volume.send_keys(1.1)

        number_of_tubes_collected_18_ml_if_some_missing = self.browser.find_element(By.ID,'id_processed_form-number_of_tubes_collected_18_ml_if_some_missing')
        number_of_tubes_collected_18_ml_if_some_missing.send_keys(1)

        all_7_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-all_7_collected'))
        all_7_collected.select_by_visible_text('No')

        partial_aliquot_7ml_volume = self.browser.find_element(By.ID,'id_processed_form-partial_aliquot_7ml_volume')
        partial_aliquot_7ml_volume.send_keys(1.1)

        number_of_tubes_collected_7_ml_if_some_missing = self.browser.find_element(By.ID,'id_processed_form-number_of_tubes_collected_7_ml_if_some_missing')
        number_of_tubes_collected_7_ml_if_some_missing.send_keys(2)

        submit = self.browser.find_element(By.XPATH,'//*[@id="processed_questions_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()


    def user_submits_urine_frozen(self):
        #id_frozen_form-freezer_placed_date_time

        freezer_placed_date_time = self.browser.find_element(By.ID, "id_frozen_form-freezer_placed_date_time")
        freezer_placed_date_time.click()
        self.choose_flatpickr_day(0)

        #id_frozen_form-number_of_tubes

        frozen_number_of_tubes = self.browser.find_element(By.ID,'id_frozen_form-number_of_tubes')
        frozen_number_of_tubes.send_keys(10)

        #id_frozen_form-notes_and_deviations

        frozen_notes = self.browser.find_element(By.ID,'id_frozen_form-notes_and_deviations')
        frozen_notes.send_keys('they were really cold')

        submit = self.browser.find_element(By.XPATH,'//*[@id="frozen_questions_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()

    def user_submits_urine_shipped_to_wsu(self):

        #user sees some of the information just entered

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Number of Tubes: 5', body)
        self.assertNotIn('Processed Date Time: None',body)
        self.assertNotIn('Stored Date Time: None', body)
        self.assertNotIn('Number of Tubes: None', body)

        self.assertIn('Logged By:',body)

        #User does not see incentive form

        self.assertNotIn('Incentive', body)

        #user submits shipped to WSu form
        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        self.scroll_into_view(shipped_date_time)
        shipped_date_time.click()
        new_num = self.choose_flatpickr_day(0)

        tracking_number = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        tracking_number.send_keys('777777')

        number_of_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        self.scroll_into_view(courier)
        courier.send_keys('FedEx')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        time.sleep(1)
        self.assertIn('Courier: FedEx',body)
        self.assertIn('Shipped By:',body)


    def user_submits_urine_received_at_wsu(self):
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Received at WSU Form', body)

        # User sees received date time at
        # user submits shipped to WSu form
        received_date_time = self.browser.find_element(By.ID, "id_received_at_wsu_form-received_date_time")
        self.scroll_into_view(received_date_time)
        received_date_time.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Received at WSU: {TODAY}', body)

        # user sees shipped to echo form

    def user_submits_urine_shipped_to_echo(self):
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped to ECHO Form',body)

        shipped_date_time = self.browser.find_element(By.ID, 'id_shipped_to_echo_form-shipped_date_and_time')
        self.scroll_into_view(shipped_date_time)
        shipped_date_time.click()
        self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Shipped Date Time: {TODAY}', body)

    def test_user_can_choose_status_of_urine_information_chooses_collected_shipped_wsu(self):
        self.user_submits_urine_collected()
        self.user_submits_urine_processed()
        self.user_submits_urine_frozen()
        self.user_submits_urine_shipped_to_wsu()
        self.user_submits_urine_received_at_wsu()
        self.user_submits_urine_shipped_to_echo()

    def test_user_can_choose_status_of_urine_information_chooses_not_collected_refused(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4101', 'U', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4101', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)
        self.assertNotIn('Declined',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees not collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text

        self.assertIn('Not Collected', body_text)
        self.assertIn('Refused', body_text)
        self.assertIn('Other', body_text)

        refused_radio = self.browser.find_element(By.ID, 'id_not_collected_form-refused_or_other_0')
        refused_radio.click()
        submit = self.browser.find_element(By.XPATH, '//*[@id="not_collected_form"]/form/input[2]')
        submit.click()
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Refused or other: Refused', body_text)
        self.assertIn('Logged By: testuser', body_text)


    def test_user_can_choose_status_of_urine_information_chooses_not_collected_other(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk('4100', 'U', trimester='S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees declined form on next page
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Not Collected Form', body_text)

        # user chooses refused
        other_radio = self.browser.find_element(By.ID, 'id_not_collected_form-refused_or_other_1')
        other_radio.click()
        other_specify = self.browser.find_element(By.ID,'other_specify_input')
        other_specify.send_keys('too busy')

        submit = self.browser.find_element(By.XPATH, '//*[@id="not_collected_form"]/form/input[2]')
        submit.click()
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn(f'Refused or other: Other', body_text)
        self.assertIn(f'Other Reason: too busy', body_text)
        self.assertIn('Logged By: testuser', body_text)

    def test_user_can_submited_urine_collected_information_and_then_leaves_and_returns_and_processed_form_is_there(
            self):
        self.user_submits_urine_collected()
        primary_key = self.return_caregiver_bio_pk('4101', 'U', trimester='S')

        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/')
        time.sleep(1)
        self.browser.get(self.live_server_url)

        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4101/{primary_key}/entry/')

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(
            'If processed and aliquoted off site, under what conditions were the tubes transported to the processing site?',
            body)
        self.assertIn(
            'What is the total volume of urine in the collection cup?',
            body)