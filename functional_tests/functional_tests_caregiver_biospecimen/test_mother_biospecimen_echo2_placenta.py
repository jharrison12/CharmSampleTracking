from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver,Project
import time
import datetime
from selenium.webdriver.support.ui import Select
from django.utils import timezone

class MotherBioSpecimenEcho2EntryTestPlacenta(FunctionalTest):

    def return_caregiver_bio_pk(self,charm_id,collection_type):
        echo2 = Project.objects.get(project_name='ECHO2')
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        project_fk=echo2)
        return caregiverbio.pk

    def test_user_can_choose_status_of_placenta_information_chooses_collected_shipped_wsu(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_no_consent'))
        collected_not_collected.select_by_visible_text('Collected')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Collected Form',form)

        #user submits form and sees data
        collected = self.browser.find_element(By.ID,"id_placenta_form-collected_date_time")
        collected.clear()
        collected.send_keys('2023-09-27 12:52:26')

        processed = self.browser.find_element(By.ID,"id_placenta_form-processed_date_time")
        processed.send_keys('2023-09-27 12:52:26')

        placed_in_formalin = self.browser.find_element(By.ID,"id_placenta_form-placed_in_formalin")
        placed_in_formalin.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        #user sees some of the information just entered

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Placed in Formalin: Sept. 27, 2023, 12:52 p.m.', body)

        self.assertIn('Logged By: testuser',body)

        #User sees incentive form

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.clear()
        incentive_date.send_keys('2023-09-27')

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Incentive Date: Sept. 27, 2023', body)

        #user sees option to choose shipped to wsu or shipped to echo


        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertNotIn('Shipped Choice Form',form)

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped to WSU Form',body)
        self.assertNotIn('tubes',body)
        self.assertNotIn('Logged date time:',body)

        #user submits shipped to WSu form
        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-shipped_date_and_time")
        shipped_date_time.clear()
        shipped_date_time.send_keys('2023-09-27 12:52:26')

        shipped_date_time = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-tracking_number")
        shipped_date_time.send_keys('777777')

        courier = self.browser.find_element(By.ID,"id_shipped_to_wsu_form-courier")
        courier.send_keys('FedEx')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_wsu_information_form"]/form/input[2]')
        submit.click()

        #user sees shipped WSU data
        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Courier: FedEx',body)
        self.assertIn('Shipped By: testuser',body)
        self.assertNotIn('Number of Tubes',body)

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Received at WSU Form',body)

        #User sees received date time at
        #user submits shipped to WSu form
        received_date_time = self.browser.find_element(By.ID,"id_received_at_wsu_form-received_date_time")
        received_date_time.clear()
        received_date_time.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH, '//*[@id="received_at_wsu_information_form"]/form/input[2]')
        submit.click()
        time.sleep(50)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Received at WSU Sept. 27, 2023, 12:52 p.m.', body)

    def test_user_can_choose_status_of_placenta_information_chooses_collected_shipped_echo(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
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
        collected = self.browser.find_element(By.ID,"id_placenta_form-collected_date_time")
        collected.clear()
        collected.send_keys('2023-09-27 12:52:26')

        stored = self.browser.find_element(By.ID,"id_placenta_form-stored_date_time")
        stored.send_keys('2023-09-27 12:52:26')

        processed = self.browser.find_element(By.ID,"id_placenta_form-processed_date_time")
        processed.send_keys('2023-09-27 12:52:26')

        number_of_tubes = self.browser.find_element(By.ID,"id_placenta_form-number_of_tubes")
        number_of_tubes.send_keys(5)

        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Number of Tubes: 5', body)

        #User sees incentive form

        incentive_date = self.browser.find_element(By.ID,'id_incentive_form-incentive_date')
        incentive_date.clear()
        incentive_date.send_keys('2023-09-27')

        submit = self.browser.find_element(By.XPATH,'//*[@id="incentive_information_form"]/form/input[2]')
        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Incentive Date: Sept. 27, 2023', body)


        #user sees option to choose shipped to wsu or shipped to echo

        form = self.browser.find_element(By.TAG_NAME,'form').text
        self.assertIn('Shipped Choice Form',form)

        shipped_to_echo = Select(self.browser.find_element(By.ID,'id_shipped_choice_form-shipped_to_wsu_or_echo'))
        shipped_to_echo.select_by_visible_text('Shipped to Echo')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_choice"]/form/input[2]')

        submit.click()


        body = self.browser.find_element(By.TAG_NAME,'body').text
        needed_div = self.browser.find_element(By.ID,'shipped_to_echo_form').text
        self.assertIn('Shipped to ECHO Form',needed_div)


        shipped_to_echo_form = self.browser.find_element(By.ID,'id_shipped_to_echo_form-shipped_date_and_time')
        shipped_to_echo_form.clear()
        shipped_to_echo_form.send_keys('2023-09-27 12:52:26')

        submit = self.browser.find_element(By.XPATH,'//*[@id="shipped_to_echo_form"]/form/input[2]')

        submit.click()

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Shipped Date Time: Sept. 27, 2023, 12:52 p.m.', body)



    def test_user_can_choose_status_of_placenta_information_chooses_not_collected(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
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

    def test_user_can_choose_status_of_placenta_information_chooses_no_consent(self):
        # User visits the caregiver biospecimen page and sees placenta
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/initial/')

        #user sees initial form and submits collected
        header_text = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Charm ID: P7000', [item.text for item in header_text])
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('Initial Form',body_text)

        collected_not_collected = Select(self.browser.find_element(By.ID,'id_initial_form-collected_not_collected_no_consent'))
        collected_not_collected.select_by_visible_text('No Consent')
        submit = self.browser.find_element(By.XPATH,'//*[@id="collected_information"]/form/input[2]')
        submit.click()

        #user sees collected form on next page

        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('<form>', body_text)
        self.assertIn('No Consent', body_text)