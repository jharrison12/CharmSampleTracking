from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dataview.models import Caregiver,Name,CaregiverName,Address,\
    CaregiverAddress, Email, CaregiverEmail,CaregiverPhone,Phone,SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,SurveyOutcome,CaregiverSurvey,Incentive,IncentiveType,Status,Collection,CaregiverBiospecimen
import datetime
import time
from django.utils import timezone
import os

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            return
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

        first_caregiver_name = Name()
        first_caregiver_name.first_name = 'Jane'
        first_caregiver_name.last_name = 'Doe'
        first_caregiver_name.save()

        second_caregiver_name = Name()
        second_caregiver_name.first_name = 'Jessica'
        second_caregiver_name.last_name = 'Smith'
        second_caregiver_name.save()

        first_caregiver_old_name = Name.objects.create(first_name='Jessica', last_name='Smith')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=first_caregiver_old_name, revision_number=2,
                                     eff_start_date=timezone.now(), status='A')

        CaregiverName.objects.create(caregiver_fk=self.second_caregiver, name_fk=second_caregiver_name, revision_number=1,
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

        phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

        phone_secondary = Phone.objects.create(area_code='666', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_secondary, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)

        twitter = SocialMedia.objects.create(social_media_name='Twitter')
        CaregiverSocialMedia.objects.create(social_media_fk=twitter, caregiver_fk=self.first_caregiver,social_media_user_name='@jonathan')
        facebook = SocialMedia.objects.create(social_media_name='Facebook')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,social_media_user_name='jonathan-h')
        facebook = SocialMedia.objects.create(social_media_name='Instagram')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,social_media_user_name='@jonathanscat')

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

        self.caregiver_prenatal_2 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_2,
                                                                   survey_outcome_fk=self.incomplete_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        #create biospecimen
        #create biospecimen

        self.completed_status = Status.objects.create(status='Completed')
        self.incomplete = Status.objects.create(status='Incomplete')
        self.urine_one = Collection.objects.create(collection_type='Urine',collection_number=1)
        self.urine_two = Collection.objects.create(collection_type='Urine',collection_number=2)
        self.serum_one = Collection.objects.create(collection_type='Serum',collection_number=1)
        self.serum_two = Collection.objects.create(collection_type='Serum',collection_number=2)        
        self.plasma_one = Collection.objects.create(collection_type='Plasma',collection_number=1)
        self.plasma_two = Collection.objects.create(collection_type='Plasma',collection_number=2)
        self.bloodspots_one = Collection.objects.create(collection_type='Bloodspots',collection_number=1)
        self.bloodspots_two = Collection.objects.create(collection_type='Bloodspots',collection_number=2)
        self.whole_blood_one = Collection.objects.create(collection_type='Whole Blood',collection_number=1)
        self.whole_blood_two = Collection.objects.create(collection_type='Whole Blood',collection_number=2)
        self.buffy_coat_one = Collection.objects.create(collection_type='Buffy Coat',collection_number=1)
        self.buffy_coat_two = Collection.objects.create(collection_type='Buffy Coat',collection_number=2)

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

        self.biospecimen_plasma_one_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.plasma_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.plasma_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_bloodspots_one_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.bloodspots_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_bloodspots_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.bloodspots_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_whole_blood_one_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.whole_blood_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_whole_blood_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.whole_blood_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_buffy_coat_one_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.completed_status,
                                                                                 collection_fk=self.buffy_coat_one,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

        self.biospecimen_buffy_coat_two_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                 status_fk=self.incomplete,
                                                                                 collection_fk=self.buffy_coat_two,
                                                                                 incentive_fk=self.incentive_one,
                                                                                 biospecimen_date=datetime.date.today())

    def tearDown(self):
        self.browser.quit()

