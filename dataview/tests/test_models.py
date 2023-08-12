import logging
from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    AddressMove,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey
import datetime
from django.utils import timezone

logging.basicConfig(level=logging.CRITICAL)

class CaregiverModelsTest(TestCase):

    def test_saving_and_retrieving_caregiver(self):
        caregiver_one = Caregiver()
        caregiver_one.charm_project_identifier = 'P7000'
        caregiver_one.date_of_birth = '1985-07-03'
        caregiver_one.ewcp_participant_identifier='0000'
        caregiver_one.echo_pin='333'
        caregiver_one.save()

        caregiver_two = Caregiver()
        caregiver_two.charm_project_identifier='P7001'
        caregiver_two.date_of_birth = '1985-07-04'
        caregiver_two.save()

        saved_caregiver = Caregiver.objects.first()
        self.assertEqual(saved_caregiver,caregiver_one)

        saved_caregivers = Caregiver.objects.all()
        self.assertEqual(saved_caregivers.count(), 2)

        first_saved_caregiver = saved_caregivers[0]
        second_saved_caregiver = saved_caregivers[1]
        self.assertEqual(first_saved_caregiver.charm_project_identifier, 'P7000')
        self.assertEqual(first_saved_caregiver.date_of_birth,datetime.date(1985, 7, 3))
        self.assertEqual(first_saved_caregiver.ewcp_participant_identifier,'0000')
        self.assertEqual(first_saved_caregiver.echo_pin,'333')
        self.assertEqual(second_saved_caregiver.charm_project_identifier, 'P7001')
        self.assertEqual(second_saved_caregiver.date_of_birth,datetime.date(1985, 7, 4))

class CaregiverNameModelsTest(TestCase):

    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')

    def test_caregiver_links_to_name_class(self):
        first_name = Name.objects.create(first_name='Jane',last_name='Doe')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver,name_fk=first_name,revision_number=1,eff_start_date=timezone.now(),status=CaregiverName.CaregiverNameStatusChoice.CURRENT)

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(caregiver_one,self.first_caregiver)

        caregiver_test = Caregiver.objects.filter(caregivername__name_fk__first_name='Jane').first()

        self.assertEqual(caregiver_test,caregiver_one)


    def test_caregiver_name_can_hold_current_name_archived_name(self):
        second_name = Name.objects.create(first_name='Jon',last_name='Smith')
        first_name = Name.objects.create(first_name='Jane',last_name='Doe')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver,name_fk=first_name,revision_number=1,eff_start_date=timezone.now(),status=CaregiverName.CaregiverNameStatusChoice.CURRENT)

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=second_name, revision_number=2,
                                     eff_start_date=timezone.now(), status=CaregiverName.CaregiverNameStatusChoice.ARCHIVED)

        caregiver_one = Caregiver.objects.first()

        caregiver_test = Caregiver.objects.filter(caregivername__name_fk__first_name='Jane').first()

        self.assertEqual(caregiver_test, caregiver_one)

        caregiver_archived = Caregiver.objects.filter(caregivername__name_fk__first_name='Jon').first()

        self.assertEqual(caregiver_archived, caregiver_one)

class CaregiverAddressModelsTest(TestCase):

    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000', participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')

        self.address = Address.objects.create(address_line_1='one drive',city='Lansing',state='MI',zip_code='38000')
        self.address_move = Address.objects.create(address_line_1='future street',address_line_2='apt 1',city='Lansing',state='MI',zip_code='38000')

        CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver,address_fk=self.address)
        CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver, address_fk=self.address_move)

    def test_caregiver_links_to_address_class(self):
        caregiver_address_test =Caregiver.objects.filter(caregiveraddress__address_fk__address_line_1='one drive').first()

        self.assertEqual(self.first_caregiver,caregiver_address_test)

    def test_caregiver_address_move_works(self):
        one_caregiver_address = AddressMove.objects.create(address_fk=self.address_move,address_move_date=datetime.date.today())

        caregiver_address_test_move =Caregiver.objects.filter(caregiveraddress__address_fk__addressmove=one_caregiver_address).first()

        self.assertEqual(self.first_caregiver,caregiver_address_test_move)


class CaregiverEmailModelsTest(TestCase):

    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000', participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')
        self.email = Email.objects.create(email='jharrison12@gmail.com')
        self.email_secondary = Email.objects.create(email='bob@gmail.com')

        CaregiverEmail.objects.create(caregiver_fk=self.first_caregiver, email_fk=self.email,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        CaregiverEmail.objects.create(caregiver_fk=self.first_caregiver, email_fk=self.email_secondary,
                                      email_type=CaregiverEmail.EmailTypeChoices.SECONDARY)

    def test_email_links_to_caregiver(self):
        caregiver_email_test = Caregiver.objects.filter(caregiveremail__email_fk__email__contains='jharrison').first()

        self.assertEqual(caregiver_email_test,self.first_caregiver)

    def test_caregiver_email_holds_primary_secondary_email(self):
        caregiver_email_test_sd = Caregiver.objects.filter(caregiveremail__email_type='SD').first()

        self.assertEqual(caregiver_email_test_sd, self.first_caregiver)

class CaregiverPhoneModelsTest(TestCase):

    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000', participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')

        self.phone = Phone.objects.create(area_code='777',phone_number='555-5555')
        self.phone_inactive = Phone.objects.create(area_code='888', phone_number='888-8888')

        CaregiverPhone.objects.create(caregiver_fk=self.first_caregiver,phone_fk=self.phone,phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)
        CaregiverPhone.objects.create(caregiver_fk=self.first_caregiver, phone_fk=self.phone_inactive, phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.INACTIVE)

        self.caregiver_one = Caregiver.objects.first()

    def test_caregiver_phone_links_to_caregiver(self):
        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_fk__phone_number__contains='555').first()

        self.assertEqual(self.caregiver_one,caregiver_phone_test)

    def test_caregiver_phone_holds_primary_inactive(self):

        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_type='IN').first()

        self.assertEqual(self.caregiver_one,caregiver_phone_test)

class CaregiverSocialMediaModelsTest(TestCase):

    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000', participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')

        self.social_media_twitter = SocialMedia.objects.create(social_media_name='Twitter')

        self.first_caregiver_social_media = CaregiverSocialMedia.objects.create(caregiver_fk=self.first_caregiver,
                                                                                social_media_fk=self.social_media_twitter,
                                                                                social_media_user_name='bob',
                                                                                social_media_consent=True)

    def test_caregiver_social_media_links_to_caregiver(self):

        first_caregiver_twitter = Caregiver.objects.filter(caregiversocialmedia__social_media_user_name='bob').first()

        self.assertEqual(first_caregiver_twitter,self.first_caregiver)

class CaregiverPersonalContactModelsTest(TestCase):

    def setUp(self):
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')
        second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',date_of_birth=datetime.date(1985,7,4),ewcp_participant_identifier='0001', participation_level_identifier='02',
                                 specimen_id='5555',echo_pin='444')

        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')

        contact_a_name = Name.objects.create(first_name='John',last_name='Smith')
        contact_b_name = Name.objects.create(first_name='Jessica',last_name='Jones')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI', zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='615',phone_number='555-5555')
        contact_b_phone = Phone.objects.create(area_code='615',phone_number='555-5556')

        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

        self.caregiver_contact_b = CaregiverPersonalContact.objects.create(caregiver_fk=first_caregiver,
                                                                           name_fk=contact_b_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_b_email,
                                                                           phone_fk=contact_b_phone,
                                                                           caregiver_contact_type='SD')

    def test_personal_contact_a_connects_to_caregiver(self):

        testing_caregiver_a = Caregiver.objects.filter(caregiverpersonalcontact__address_fk__address_line_1='two drive').first()

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(testing_caregiver_a,caregiver_one)

    def test_personal_contact_b_connects_to_caregiver(self):

        testing_caregiver_a = Caregiver.objects.filter(caregiverpersonalcontact__phone_fk__phone_number='555-5556').first()

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(testing_caregiver_a,caregiver_one)

    def test_caregiver_a_has_two_personal_contacts(self):
        caregiver_one = Caregiver.objects.first()
        personal_contacts = CaregiverPersonalContact.objects.filter(caregiver_fk=caregiver_one)

        self.assertEqual(personal_contacts.count(),2)

class CaregiverSurveyModelsTest(TestCase):
    def setUp(self):
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')
        second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',date_of_birth=datetime.date(1985,7,4),ewcp_participant_identifier='0001', participation_level_identifier='02',
                                 specimen_id='5555',echo_pin='444')

        self.new_project = Project.objects.create(project_name='MARCH')

        self.new_survey = Survey.objects.create(survey_name='Prenatal 1',project_fk=self.new_project)

    def test_survey_associated_with_project(self):
        test_survey = Survey.objects.filter()
