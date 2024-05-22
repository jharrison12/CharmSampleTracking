import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
from functional_tests.base import FunctionalTest,TODAY
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone
logging.basicConfig(level=logging.debug)



class MotherBioSpecimenEcho2EntryTestBlood(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type,trimester,project='ECHO2'):
        logging.debug(f"{charm_id} {collection_type} {trimester}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def click_outside_of_element(self,html_id):
        self.browser.find_element(By.ID,html_id).click()

    def user_input_collected_blood(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        # user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Initial Form', body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID, 'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees collected form on next page
        time.sleep(1)
        form = self.browser.find_element(By.ID, 'collected_information_form').text
        self.assertIn('Collected Form',form)

        # user submits form and sees data

        eat_or_drink = self.browser.find_element(By.ID, "id_blood_form-other_water_date_time")
        eat_or_drink.click()
        number_of_elements = self.choose_flatpickr_day(0)

        self.browser.find_element(By.TAG_NAME,'body').click()
        collected = self.browser.find_element(By.ID, "id_blood_form-collected_date_time")
        collected.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)
        time.sleep(1)

        #user chooses partial for tube #1

        tube_number_1 = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_1'))
        tube_number_1.select_by_visible_text('Partial')

        tube_number_1_estimated = self.browser.find_element(By.ID,'id_blood_form-tube_1_estimated_volume')
        tube_number_1_estimated.send_keys(1)

        # id_blood_form-tube_1_hemolysis
        tube_number_1_hemolysis = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_1_hemolysis'))
        tube_number_1_hemolysis.select_by_visible_text('Mild')

        # id_blood_form-tube_2
        tube_number_2 = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_2'))
        tube_number_2.select_by_visible_text('Partial')
        tube_number_2_estimated = self.browser.find_element(By.ID,'id_blood_form-tube_2_estimated_volume')
        tube_number_2_estimated.send_keys(2)
        tube_number_2_hemolysis = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_2_hemolysis'))
        tube_number_2_hemolysis.select_by_visible_text('Severe')

        # id_blood_form-tube_2
        tube_number_3 = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_3'))
        tube_number_3.select_by_visible_text('Partial')
        tube_number_3_estimated = self.browser.find_element(By.ID,'id_blood_form-tube_3_estimated_volume')
        tube_number_3_estimated.send_keys(3)
        tube_number_3_hemolysis = Select(self.browser.find_element(By.ID, 'id_blood_form-tube_3_hemolysis'))
        tube_number_3_hemolysis.select_by_visible_text('Severe')

        submit = self.browser.find_element(By.XPATH, '//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        collected_blood_information = self.browser.find_element(By.ID,'collected_blood_information').text
        self.assertIn('Complete or Partial: Partial',collected_blood_information)
        self.assertIn('Estimated Volume: 1.0',collected_blood_information)


    def user_inputs_processed_blood_information(self):
        body = self.browser.find_element(By.TAG_NAME, 'body').text

    #     id_processed_form-processed_aliquoted_off_site

        processed_aliquoted_off_site = Select(self.browser.find_element(By.ID, 'id_processed_form-processed_aliquoted_off_site'))
        processed_aliquoted_off_site.select_by_visible_text('Refrigerated')

        processed_received_date_time = self.browser.find_element(By.ID, "id_processed_form-specimen_received_date_time")
        processed_received_date_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        refrigerated_prior_to_centrifuge = Select(self.browser.find_element(By.ID, 'id_processed_form-edta_purple_tube_refrigerated_prior_to_centrifuge'))
        refrigerated_prior_to_centrifuge.select_by_visible_text('Yes')

        edta_purple_refrigerated_placed_date_time = self.browser.find_element(By.ID, "id_processed_form-edta_purple_refrigerated_placed_date_time")
        edta_purple_refrigerated_placed_date_time.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        edta_purple_refrigerated_removed_date_time = self.browser.find_element(By.ID, "id_processed_form-edta_purple_refrigerated_removed_date_time")
        self.scroll_into_view(edta_purple_refrigerated_removed_date_time)
        edta_purple_refrigerated_removed_date_time.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        #id_processed_form-whole_blood_blue_cap_all_collected
        whole_blood_blue_cap_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-whole_blood_blue_cap_all_collected'))
        whole_blood_blue_cap_all_collected.select_by_visible_text('No')

        whole_blood_blue_cap_partial_aliquot_volume = self.browser.find_element(By.ID, "id_processed_form-whole_blood_blue_cap_partial_aliquot_volume")
        whole_blood_blue_cap_partial_aliquot_volume.send_keys(1.0)

        whole_blood_blue_cap_number_collected = self.browser.find_element(By.ID, "id_processed_form-whole_blood_blue_cap_number_collected")
        whole_blood_blue_cap_number_collected.send_keys(1)

        blood_spot_card_completed = Select(self.browser.find_element(By.ID, 'id_processed_form-blood_spot_card_completed'))
        blood_spot_card_completed.select_by_visible_text('No')

        blood_spot_card_number_of_dots_smaller_than_dotted_circle = self.browser.find_element(By.ID, "id_processed_form-blood_spot_card_number_of_dots_smaller_than_dotted_circle")
        blood_spot_card_number_of_dots_smaller_than_dotted_circle.send_keys(2)

        blood_spot_card_number_of_complete_spots = self.browser.find_element(By.ID,"id_processed_form-blood_spot_card_number_of_complete_spots")
        blood_spot_card_number_of_complete_spots.send_keys(2)

        blood_spot_card_number_of_dotted_circle_missing_blood_spot = self.browser.find_element(By.ID,"id_processed_form-blood_spot_card_number_of_dotted_circle_missing_blood_spot")
        blood_spot_card_number_of_dotted_circle_missing_blood_spot.send_keys(2)

        vacutainer_centrifuge_start_time = self.browser.find_element(By.ID, "id_processed_form-vacutainer_centrifuge_start_time")
        self.scroll_into_view(vacutainer_centrifuge_start_time)
        vacutainer_centrifuge_start_time.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)
        self.click_outside_of_element("id_processed_form-blood_spot_card_number_of_dotted_circle_missing_blood_spot")

        vacutainer_centrifuge_end_time = self.browser.find_element(By.ID, "id_processed_form-vacutainer_centrifuge_end_time")
        self.scroll_into_view(vacutainer_centrifuge_end_time)
        vacutainer_centrifuge_end_time.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        plasma_purple_cap_200_microliter_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-plasma_purple_cap_200_microliter_all_collected'))
        plasma_purple_cap_200_microliter_all_collected.select_by_visible_text('No')

        plasma_purple_cap_200_microliter_number_collected = self.browser.find_element(By.ID,"id_processed_form-plasma_purple_cap_200_microliter_number_collected")
        plasma_purple_cap_200_microliter_number_collected.send_keys(2)

        plasma_purple_cap_1_ml_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-plasma_purple_cap_1_ml_all_collected'))
        plasma_purple_cap_1_ml_all_collected.select_by_visible_text('No')

        plasma_purple_cap_1_ml_partial_aliquot_volume = self.browser.find_element(By.ID,"id_processed_form-plasma_purple_cap_1_ml_partial_aliquot_volume")
        plasma_purple_cap_1_ml_partial_aliquot_volume.send_keys(0.98)

        plasma_purple_cap_1_ml_number_collected = self.browser.find_element(By.ID,"id_processed_form-plasma_purple_cap_1_ml_number_collected")
        plasma_purple_cap_1_ml_number_collected.send_keys(2)

        buffy_coat_green_cap_1_ml_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-buffy_coat_green_cap_1_ml_all_collected'))
        buffy_coat_green_cap_1_ml_all_collected.select_by_visible_text('No')

        buffy_coat_green_cap_1_ml_number_collected = self.browser.find_element(By.ID,"id_processed_form-buffy_coat_green_cap_1_ml_number_collected")
        buffy_coat_green_cap_1_ml_number_collected.send_keys(2)

        red_blood_cells_yellow_cap_1_ml_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-red_blood_cells_yellow_cap_1_ml_all_collected'))
        red_blood_cells_yellow_cap_1_ml_all_collected.select_by_visible_text('No')

        red_blood_cells_yellow_cap_1_ml_partial_aliquot_volume = self.browser.find_element(By.ID,"id_processed_form-red_blood_cells_yellow_cap_1_ml_partial_aliquot_volume")
        red_blood_cells_yellow_cap_1_ml_partial_aliquot_volume.send_keys(1.3)

        red_blood_cells_yellow_cap_1_ml_number_collected = self.browser.find_element(By.ID,"id_processed_form-red_blood_cells_yellow_cap_1_ml_number_collected")
        red_blood_cells_yellow_cap_1_ml_number_collected.send_keys(2)

        serum_red_cap_200_microl_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-serum_red_cap_200_microl_all_collected'))
        serum_red_cap_200_microl_all_collected.select_by_visible_text('No')

        serum_red_cap_200_microl_number_collected = self.browser.find_element(By.ID,"id_processed_form-serum_red_cap_200_microl_number_collected")
        serum_red_cap_200_microl_number_collected.send_keys(2)

        serum_red_cap_1_ml_all_collected = Select(self.browser.find_element(By.ID, 'id_processed_form-serum_red_cap_1_ml_all_collected'))
        serum_red_cap_1_ml_all_collected.select_by_visible_text('No')

        serum_red_cap_1_ml_partial_aliquot_volume = self.browser.find_element(By.ID,"id_processed_form-serum_red_cap_1_ml_partial_aliquot_volume")
        serum_red_cap_1_ml_partial_aliquot_volume.send_keys(0.9)

        serum_red_cap_1_ml_number_collected = self.browser.find_element(By.ID,"id_processed_form-serum_red_cap_1_ml_number_collected")
        serum_red_cap_1_ml_number_collected.send_keys(2)


        submit = self.browser.find_element(By.XPATH, '//*[@id="processed_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()


    def user_inputs_frozen_information(self):
        freezer_placed_date_time = self.browser.find_element(By.ID, "id_frozen_form-freezer_placed_date_time")
        self.scroll_into_view(freezer_placed_date_time)
        freezer_placed_date_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        number_of_tubes = self.browser.find_element(By.ID,"id_frozen_form-number_of_tubes")
        number_of_tubes.send_keys(2)

        blood_spot_card_placed_in_freezer = self.browser.find_element(By.ID, "id_frozen_form-blood_spot_card_placed_in_freezer")
        self.scroll_into_view(blood_spot_card_placed_in_freezer)
        blood_spot_card_placed_in_freezer.click()
        number_of_elements = self.choose_flatpickr_day(number_of_elements)

        notes_and_deviations = self.browser.find_element(By.ID,"id_frozen_form-notes_and_deviations")
        notes_and_deviations.send_keys("great")

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()


    def user_inputs_shipped_to_wsu_blood(self):
        shipped_date_and_time = self.browser.find_element(By.ID, "id_shipped_to_wsu_form-shipped_date_and_time")
        self.scroll_into_view(shipped_date_and_time)
        shipped_date_and_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        number_of_tubes = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-number_of_tubes")
        number_of_tubes.send_keys(2)

        courier = Select(self.browser.find_element(By.ID, 'id_shipped_to_wsu_form-courier'))
        courier.select_by_visible_text('FedEx')

        tracking_number = self.browser.find_element(By.ID, "id_shipped_to_wsu_form-tracking_number")
        tracking_number.send_keys(4444444)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()

    def user_inputs_received_at_wsu_blood(self):
        received_date_time = self.browser.find_element(By.ID, "id_received_at_wsu_form-received_date_time")
        self.scroll_into_view(received_date_time)
        received_date_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()

    def user_inputs_shipped_echo_blood_page(self):
        shipped_date_and_time = self.browser.find_element(By.ID, "id_shipped_to_echo_form-shipped_date_and_time")
        self.scroll_into_view(shipped_date_and_time)
        shipped_date_and_time.click()
        number_of_elements = self.choose_flatpickr_day(0)

        submit = self.browser.find_element(By.XPATH, '//*[@id="shipped_to_echo_form"]/form/input[2]')
        self.scroll_into_view(submit)
        submit.click()

        time.sleep(30)


    def test_user_can_choose_status_of_blood_information_chooses_collected_processed_shipped_to_wsu_received_wsu_shipped_echo(self):
        self.user_input_collected_blood()

        self.user_inputs_processed_blood_information()

        self.user_inputs_frozen_information()

        self.user_inputs_shipped_to_wsu_blood()

        self.user_inputs_received_at_wsu_blood()

        self.user_inputs_shipped_echo_blood_page()

    def test_user_can_choose_status_of_blood_information_chooses_not_collected_other(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B', trimester='S')
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
        time.sleep(2)
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

    def test_user_can_choose_status_of_blood_information_chooses_not_collected_refused(self):
        # User visits the caregiver biospecimen page and sees blood
        primary_key = self.return_caregiver_bio_pk('4100', 'B',trimester='S')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/4100/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: 4100', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected'))
        collected_not_collected.select_by_visible_text('Not Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        # user sees declined form on next page
        time.sleep(2)
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Not Collected Form', body_text)

        #user chooses refused

        refused_radio = self.browser.find_element(By.ID, 'id_not_collected_form-refused_or_other_0')
        refused_radio.click()
        submit = self.browser.find_element(By.XPATH, '//*[@id="not_collected_form"]/form/input[2]')
        submit.click()
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Refused or other: Refused', body_text)
        self.assertIn('Logged By: testuser', body_text)

    def test_user_can_submited_blood_collected_information_and_then_leaves_and_returns_and_processed_form_is_there(self):
        self.fail()