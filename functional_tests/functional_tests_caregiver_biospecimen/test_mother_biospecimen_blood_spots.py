from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest
from biospecimen.models import CaregiverBiospecimen,Caregiver
import time
import datetime
from selenium.webdriver.support.ui import Select

class MotherBioSpecimenBloodspotsTest(FunctionalTest):


    def return_caregiver_bio_pk(self,charm_id,collection_type,collection_num,trimester=None,project="ECHO1"):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        if trimester is not None:
            caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                            collection_fk__collection_type_fk__collection_type=collection_type,
                                                            trimester_fk__trimester=trimester,
                                                            project_fk__project_name=project)
        else:
            caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        collection_fk__collection_number_fk__collection_number=collection_num,
                                                            project_fk__project_name=project)

        return caregiverbio.pk

    def test_user_can_see_bio_blood_spot_information(self):
        # User visits the caregiver biospecimen page and sees urine
        primary_key = self.return_caregiver_bio_pk(charm_id='P7000',collection_type='Bloodspots',collection_num='F')
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}biospecimen/caregiver/P7000/{primary_key}/history/')

        header_text = self.browser.find_elements(By.TAG_NAME,'h1')
        self.assertIn('Charm ID: P7000 Family ID: 4444',[item.text for item in header_text])

        body = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn("ID: 1111BS", body)
        self.assertIn("Log Status: Completed", body)

        #User sees processed information if there is processed data
        self.assertIn('Collected Date Time:May 5, 2023, 8 a.m.',body)
        self.assertIn('Quantity: 2',body)
        self.assertIn('Logged Date Time:May 5, 2023, 8 a.m.',body)
        self.assertIn('Processed Date Time:May 5, 2023, 8:04 a.m.',body)
        ##TODO change
        self.assertIn('Logged By:BLANK',body)

        # #user goes to a respondent without processed data and sees a form!

        #user sees shipped data just submitted.

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity:19',body)
        self.assertIn('Shipping Number:7777777',body)
        self.assertIn('Courier:Fedex',body)

        #user goes to P7000 to see stored data
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Quantity:19',body)
        self.assertIn('Storage Location:MSU',body)

