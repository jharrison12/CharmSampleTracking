from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress, Email, CaregiverEmail,CaregiverPhone,Phone
import datetime
import time
from django.utils import timezone

MAX_WAIT =10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000',
                                                   participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')
        second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
                                                    date_of_birth=datetime.date(1985, 7, 4),
                                                    ewcp_participant_identifier='0001',
                                                    participation_level_identifier='02',
                                                    specimen_id='5555', echo_pin='444')

        first_caregiver_name = Name()
        first_caregiver_name.first_name = 'Jane'
        first_caregiver_name.last_name = 'Doe'
        first_caregiver_name.save()

        second_caregiver_name = Name()
        second_caregiver_name.first_name = 'Jessica'
        second_caregiver_name.last_name = 'Smith'
        second_caregiver_name.save()

        first_caregiver_old_name = Name.objects.create(first_name='Jessica', last_name='Smith')

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_old_name, revision_number=2,
                                     eff_start_date=timezone.now(), status='A')

        CaregiverName.objects.create(caregiver_fk=second_caregiver, name_fk=second_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        # Create address
        address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=first_caregiver, address_fk=address)

        address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=second_caregiver, address_fk=address2)

        # Create email
        email = Email.objects.create(email='jharrison12@gmail.com')
        CaregiverEmail.objects.create(email_fk=email, caregiver_fk=first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        email_secondary = Email.objects.create(email='f@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_secondary, caregiver_fk=first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.SECONDARY)

        email_archived = Email.objects.create(email='INACTIVE@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_archived, caregiver_fk=first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.INACTIVE)

        email2 = Email.objects.create(email='jharrison13@gmail.com')
        CaregiverEmail.objects.create(email_fk=email2, caregiver_fk=second_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

    def tearDown(self):
        self.browser.quit()


    def test_user_can_view_web_page_of_mother_ids(self):
        #User visits the initial page and is given a list of mother ids
        home_page = self.live_server_url
        self.browser.get(self.live_server_url)
        self.assertIn('Charm Sample Tracking', self.browser.title)

        #User sees a list of mother ids
        link_text = self.browser.find_element(By.LINK_TEXT,'Mother Sample').text
        self.assertIn('Mother Sample', link_text)

        #User types in link to caregiver page
        self.browser.get(f'{self.browser.current_url}data/caregiver')

        #User looks for one caregiver id in page
        body_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertIn('P7000',body_text)
        #User sees the other charm project sampleid
        self.assertIn('P7001',body_text)

        #User visits the page for P7000
        ## Is there a better way of navigating using selenium?
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7000')
        header_text_id_page = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Mothers name is: Doe, Jane',header_text_id_page)

        body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('July 3, 1985',body_text_id_page)
        self.assertIn('P7000',body_text_id_page)
        self.assertIn('0000',body_text_id_page)
        self.assertIn('01',body_text_id_page)
        self.assertIn('Echo Pin: 333',body_text_id_page)
        self.assertIn('Specimen Id: 4444',body_text_id_page)
        self.assertIn('Address: One Drive', body_text_id_page)
        self.assertIn('Lansing', body_text_id_page)
        self.assertIn('MI', body_text_id_page)
        self.assertIn('38000', body_text_id_page)
        self.assertIn('Email Primary: jharrison12@gmail.com', body_text_id_page)
        self.assertIn('Email Secondary: f@gmail.com', body_text_id_page)
        self.assertIn('Primary Phone: 555-555-5555', body_text_id_page)



        #User visits the page for P7001
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}data/caregiver/P7001')
        body_text_id_page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('P7001', body_text_id_page)




