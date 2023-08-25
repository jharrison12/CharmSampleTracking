import logging
import unittest

from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    AddressMove,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,SurveyOutcome,CaregiverSurvey,Incentive,IncentiveType,Status,Collection,CaregiverBiospecimen
import datetime
from django.utils import timezone

logging.basicConfig(level=logging.CRITICAL)

class TestCaseSetup(TestCase):
    def setUp(self):

        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000',
                                                   participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')
        self.second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
                                                    date_of_birth=datetime.date(1985, 7, 4),
                                                    ewcp_participant_identifier='0001',
                                                    participation_level_identifier='02',
                                                    specimen_id='5555', echo_pin='444')

        self.first_caregiver_name = Name()
        self.first_caregiver_name.first_name = 'Jane'
        self.first_caregiver_name.last_name = 'Doe'
        self.first_caregiver_name.save()

        self.second_caregiver_name = Name()
        self.second_caregiver_name.first_name = 'Jessica'
        self.second_caregiver_name.last_name = 'Smith'
        self.second_caregiver_name.save()

        self.first_caregiver_old_name = Name.objects.create(first_name='Sandy', last_name='Cheeks')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_old_name,
                                     revision_number=2,
                                     eff_start_date=timezone.now(), status='A')

        CaregiverName.objects.create(caregiver_fk=self.second_caregiver, name_fk=self.second_caregiver_name,
                                     revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        # Create address
        address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver, address_fk=address)

        address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=self.second_caregiver, address_fk=address2)

        # Create email
        email = Email.objects.create(email='jharrison12@gmail.com')
        CaregiverEmail.objects.create(email_fk=email, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        email_secondary = Email.objects.create(email='f@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_secondary, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.SECONDARY)

        email_archived = Email.objects.create(email='INACTIVE@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_archived, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.INACTIVE)

        email2 = Email.objects.create(email='jharrison13@gmail.com')
        CaregiverEmail.objects.create(email_fk=email2, caregiver_fk=self.second_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        # Create phone
        phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

        phone_secondary = Phone.objects.create(area_code='666', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_secondary, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)

        phone_archived = Phone.objects.create(area_code='777', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_archived, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.INACTIVE)

        # Create social media
        twitter = SocialMedia.objects.create(social_media_name='Twitter')
        CaregiverSocialMedia.objects.create(social_media_fk=twitter, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='@jonathan')
        facebook = SocialMedia.objects.create(social_media_name='Facebook')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='jonathan-h')
        facebook = SocialMedia.objects.create(social_media_name='Instagram')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='@jonathanscat')

        # Create caregiver
        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')
        contact_c_email = Email.objects.create(email='d@d.com')

        contact_a_name = Name.objects.create(first_name='John', last_name='Jones')
        contact_b_name = Name.objects.create(first_name='Jessica', last_name='Jones')
        contact_c_name = Name.objects.create(first_name='James', last_name='Contact')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI',
                                                   zip_code='38000')
        contact_c_address = Address.objects.create(address_line_1='three drive', city='East Lansing', state='MI',
                                                   zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='999', phone_number='999-9999')
        contact_b_phone = Phone.objects.create(area_code='999', phone_number='999-9998')
        contact_c_phone = Phone.objects.create(area_code='999', phone_number='999-9997')

        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=self.first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

        self.caregiver_contact_b = CaregiverPersonalContact.objects.create(caregiver_fk=self.first_caregiver,
                                                                           name_fk=contact_b_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_b_email,
                                                                           phone_fk=contact_b_phone,
                                                                           caregiver_contact_type='SD')

        self.caregiver_contact_b = CaregiverPersonalContact.objects.create(caregiver_fk=self.second_caregiver,
                                                                           name_fk=contact_c_name,
                                                                           address_fk=contact_c_address,
                                                                           email_fk=contact_c_email,
                                                                           phone_fk=contact_c_phone,
                                                                           caregiver_contact_type='PR')

        #Create surveys


        self.new_project = Project.objects.create(project_name='MARCH')

        self.prenatal_1 = Survey.objects.create(survey_name='Prenatal 1', project_fk=self.new_project)
        self.prenatal_2 = Survey.objects.create(survey_name='Prenatal 2', project_fk=self.new_project)

        self.completed_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Completed')
        self.incomplete_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Incomplete')

        self.incentive_type_one = IncentiveType.objects.create(incentive_type_text='Gift Card')

        self.incentive_one = Incentive.objects.create(incentive_type_fk=self.incentive_type_one,
                                                      incentive_date=datetime.date.today(), incentive_amount=100)

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_2,
                                                                   survey_outcome_fk=self.incomplete_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        # create biospecimen
        #create biospecimen

        self.completed_status = Status.objects.create(status='Completed')
        self.incomplete = Status.objects.create(status='Incomplete')
        self.urine_one = Collection.objects.create(collection_type='Urine',collection_number=1)
        self.urine_two = Collection.objects.create(collection_type='Urine',collection_number=2)
        self.serum_one = Collection.objects.create(collection_type='Serum',collection_number=1)
        self.serum_two = Collection.objects.create(collection_type='Serum',collection_number=2)
        self.plasma_one = Collection.objects.create(collection_type='plasma',collection_number=1)
        self.plasma_two = Collection.objects.create(collection_type='plasma',collection_number=2)

        self.biospecimen_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                   status_fk=self.completed_status,
                                                                   collection_fk=self.urine_one,
                                                                   incentive_fk=self.incentive_one,
                                                                   biospecimen_date=datetime.date.today())

        self.biospecimen_two_caregiver_two = CaregiverBiospecimen.objects.create(caregiver_fk=self.second_caregiver,
                                                                   status_fk=self.completed_status,
                                                                   collection_fk=self.urine_one,
                                                                   incentive_fk=self.incentive_one,
                                                                   biospecimen_date=datetime.date.today())

        self.biospecimen_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.urine_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_serum_one_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.serum_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_serum_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.serum_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.plasma_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.plasma_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

# Create your tests here.
class HomePageTest(TestCaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')

class CaregiverPageTest(TestCaseSetup):

    def test_caregiver_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/')
        self.assertTemplateUsed(response, 'dataview/caregiver.html')

    def test_mother_page_contains_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        response = self.client.get(f'/data/caregiver/')
        self.assertContains(response,'P7000')

    def test_mother_page_contains_second_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        Caregiver.objects.create(charm_project_identifier='P7001')
        response = self.client.get(f'/data/caregiver/')
        self.assertContains(response,'P7001')

class CaregiverInformationPageTest(TestCaseSetup):

    def test_caregiver_information_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/P7000/')
        self.assertTemplateUsed(response,'dataview/caregiver_info.html')

    def test_caregiver_info_page_contains_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'P7000')

    def test_other_caregiver_info_page_contains_other_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7001/')
        self.assertNotContains(response,'P7000')
        self.assertContains(response,'P7001')

    def test_caregiver_information_page_contains_birthday(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'July 3, 1985')

    def test_caregiver_information_page_contains_ewcp(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '0000')

    def test_caregiver_information_page_contains_participation_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '01')

    def test_caregiver_information_page_contains_echo_pin(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '333')

    def test_caregiver_information_page_contains_specimen_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '4444')

    def test_caregiver_information_page_contains_active_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')

    def test_caregiver_information_page_does_not_contain_archived_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, 'Sandy')
        self.assertNotContains(response, 'Cheeks')

    def test_caregiver_information_page_contains_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'One Drive')

    def test_caregiver_information_page_shows_primary_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'jharrison12@gmail.com')

    def test_caregiver_information_page_shows_secondary_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'f@gmail.com')

    def test_caregiver_information_page_does_not_show_archived_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, 'INACTIVE@gmail.com')

    def test_caregiver_information_page_shows_primary_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '555-555-5555')

    def test_caregiver_information_page_shows_secondary_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '666-666-6666')

    def test_caregiver_information_page_does_not_show_inactive_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, '777-666-6666')

    def test_caregiver_information_page_shows_social_media_handle(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Twitter: @jonathan')
        self.assertContains(response,'Facebook: jonathan-h')
        self.assertContains(response,'Instagram: @jonathanscat')

    def test_caregiver_information_page_shows_contact_a_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A First Name: John')
        self.assertContains(response,'Contact A Last Name: Jones')

    def test_caregiver_information_page_shows_contact_a_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Phone Number: 999-999-9999')

    def test_caregiver_information_page_shows_contact_a_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Address: two drive')

    def test_caregiver_information_page_shows_contact_a_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Email: b@b.com')

    def test_caregiver_information_page_shows_contact_b_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B First Name: Jessica')
        self.assertContains(response,'Contact B Last Name: Jones')

    def test_caregiver_information_page_shows_contact_b_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Phone Number: 999-999-9998')

    def test_caregiver_information_page_shows_contact_b_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Address: two drive')

    def test_caregiver_information_page_shows_contact_b_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Email: c@c.com')

    def test_caregiver_information_page_does_not_show_contact_b_if_it_does_not_exist(self):
        response = self.client.get(f'/data/caregiver/P7001/')
        self.assertNotContains(response,'Contact B')


class CaregiverSurveyPageTest(TestCaseSetup):

    def test_caregiver_survey_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertTemplateUsed(response, 'dataview/caregiver_survey.html')

    def test_caregiver_survey_page_shows_prenatal1_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 1: Complete')

    def test_caregiver_survey_page_shows_prenatal2_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 2: Incomplete')

class CaregiverBiospecimenPageTest(TestCaseSetup):

    def test_caregiver_biospecimen_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertTemplateUsed(response,'dataview/caregiver_biospecimen.html')

    def test_caregiver_biospecimen_page_contains_urine_1(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response,'Serum 1: Completed')

    def test_caregiver_b_biospecimen_does_not_appear_in_caregiver_a_page(self):
        response = self.client.get(f'/data/caregiver/P7001/biospecimen/')
        self.assertNotContains(response,'Serum 1: Completed')