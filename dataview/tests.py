import logging
import unittest

from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    AddressMove,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact
import datetime
from django.utils import timezone

logging.basicConfig(level=logging.CRITICAL)

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')

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

class CaregiverSocialMediaTest(TestCase):

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

class CaregiverPersonalContactTest(TestCase):

    def setUp(self):
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')
        second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',date_of_birth=datetime.date(1985,7,4),ewcp_participant_identifier='0001', participation_level_identifier='02',
                                 specimen_id='5555',echo_pin='444')

        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')

        contact_a_name = Name.objects.create(first_name='John',last_name='Smith')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI', zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='615',phone_number='555-5555')

        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

    def test_personal_contact_a_connects_to_caregiver(self):

        testing_caregiver_a = Caregiver.objects.filter(caregiverpersonalcontact__address_fk__address_line_1='two drive').first()

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(testing_caregiver_a,caregiver_one)


class CaregiverPageTest(TestCase):

    def test_caregiver_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver')
        self.assertTemplateUsed(response, 'dataview/caregiver.html')

    def test_mother_page_contains_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        response = self.client.get(f'/data/caregiver')
        self.assertContains(response,'P7000')

    def test_mother_page_contains_second_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        Caregiver.objects.create(charm_project_identifier='P7001')
        response = self.client.get(f'/data/caregiver')
        self.assertContains(response,'P7001')

class CaregiverInformationPageTest(TestCase):

    def setUp(self):
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')
        second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',date_of_birth=datetime.date(1985,7,4),ewcp_participant_identifier='0001', participation_level_identifier='02',
                                 specimen_id='5555',echo_pin='444')

        first_caregiver_name = Name()
        first_caregiver_name.first_name = 'Jane'
        first_caregiver_name.last_name = 'Doe'
        first_caregiver_name.save()

        second_caregiver_name = Name()
        second_caregiver_name.first_name = 'Jessica'
        second_caregiver_name.last_name = 'Smith'
        second_caregiver_name.save()

        first_caregiver_old_name = Name.objects.create(first_name='Jessica',last_name='Smith')

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(),status='C')

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_old_name, revision_number=2,
                                     eff_start_date=timezone.now(),status='A')

        CaregiverName.objects.create(caregiver_fk=second_caregiver, name_fk=second_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(),status='C')

        #Create address
        address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=first_caregiver, address_fk=address)

        address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=second_caregiver, address_fk=address2)

        #Create email
        email = Email.objects.create(email='jharrison12@gmail.com')
        CaregiverEmail.objects.create(email_fk=email,caregiver_fk=first_caregiver,email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        email_secondary = Email.objects.create(email='f@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_secondary,caregiver_fk=first_caregiver,email_type=CaregiverEmail.EmailTypeChoices.SECONDARY)

        email_archived = Email.objects.create(email='INACTIVE@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_archived, caregiver_fk=first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.INACTIVE)

        email2 = Email.objects.create(email='jharrison13@gmail.com')
        CaregiverEmail.objects.create(email_fk=email2,caregiver_fk=second_caregiver,email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        #Create phone
        phone = Phone.objects.create(area_code='555',phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone,caregiver_fk=first_caregiver,phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

        phone_secondary = Phone.objects.create(area_code='666', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_secondary, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)

        phone_archived = Phone.objects.create(area_code='777', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_archived, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.INACTIVE)

        #Create social media
        twitter = SocialMedia.objects.create(social_media_name='Twitter')
        CaregiverSocialMedia.objects.create(social_media_fk=twitter, caregiver_fk=first_caregiver,social_media_user_name='@jonathan')
        facebook = SocialMedia.objects.create(social_media_name='Facebook')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=first_caregiver,social_media_user_name='jonathan-h')
        facebook = SocialMedia.objects.create(social_media_name='Instagram')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=first_caregiver,social_media_user_name='@jonathanscat')

        #Create caregiver
        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')

        contact_a_name = Name.objects.create(first_name='John', last_name='Jones')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI',
                                                   zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='615', phone_number='555-5555')

        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

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
        self.assertNotContains(response, 'Jessica')
        self.assertNotContains(response, 'Smith')

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


class CaregiverContactPageTest(TestCase):

    def setUp(self):

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

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_old_name,
                                     revision_number=2,
                                     eff_start_date=timezone.now(), status='A')

        CaregiverName.objects.create(caregiver_fk=second_caregiver, name_fk=second_caregiver_name,
                                     revision_number=1,
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

        # Create phone
        phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

        phone_secondary = Phone.objects.create(area_code='666', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_secondary, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)

        phone_archived = Phone.objects.create(area_code='777', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_archived, caregiver_fk=first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.INACTIVE)

        # Create social media
        twitter = SocialMedia.objects.create(social_media_name='Twitter')
        CaregiverSocialMedia.objects.create(social_media_fk=twitter, caregiver_fk=first_caregiver,
                                            social_media_user_name='@jonathan')
        facebook = SocialMedia.objects.create(social_media_name='Facebook')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=first_caregiver,
                                            social_media_user_name='jonathan-h')
        facebook = SocialMedia.objects.create(social_media_name='Instagram')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=first_caregiver,
                                            social_media_user_name='@jonathanscat')

        # Create caregiver
        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')

        contact_a_name = Name.objects.create(first_name='John', last_name='Jones')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI',
                                                   zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='999', phone_number='999-9999')

        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

    def test_caregiver_contact_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/P7000/contact/')
        self.assertTemplateUsed(response, 'dataview/caregiver_contact.html')

    def test_caregiver_contact_page_contains_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7000/contact/')
        self.assertContains(response,'P7000')

    def test_caregiver_information_page_shows_contact_a_name(self):
        response = self.client.get(f'/data/caregiver/P7000/contact/')
        self.assertContains(response,'Contact A First Name: John')

    def test_caregiver_information_page_shows_contact_a_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/contact/')
        self.assertContains(response,'Contact A Phone Number: 999-999-9999')

    def test_caregiver_information_page_shows_contact_a_address(self):
        response = self.client.get(f'/data/caregiver/P7000/contact/')
        self.assertContains(response,'Contact A Address: two drive')

    def test_caregiver_information_page_shows_contact_a_email(self):
        response = self.client.get(f'/data/caregiver/P7000/contact/')
        self.assertContains(response,'Contact A Email: b@b.com')