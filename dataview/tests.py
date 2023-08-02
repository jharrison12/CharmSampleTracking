import logging
from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress
import datetime
from django.utils import timezone

logging.basicConfig(level=logging.DEBUG)

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

class CaregiverNameTest(TestCase):

    def test_caregiver_links_to_name_class(self):
        first_name = Name.objects.create(first_name='Jane',last_name='Doe')
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01',
                                 specimen_id='4444',echo_pin='333')
        CaregiverName.objects.create(caregiver_fk=first_caregiver,name_fk=first_name,revision_number=1,eff_start_date=timezone.now())

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(caregiver_one,first_caregiver)

        caregiver_test = Caregiver.objects.filter(caregivername__name_fk__first_name='Jane').first()

        self.assertEqual(caregiver_test,caregiver_one)

class CaregiverAddressTest(TestCase):
    def test_caregiver_links_to_address_class(self):
        address = Address.objects.create(address_line_1='one drive',city='Lansing',state='MI',zip_code='38000')
        first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                   date_of_birth=datetime.date(1985, 7, 3),
                                                   ewcp_participant_identifier='0000', participation_level_identifier='01',
                                                   specimen_id='4444', echo_pin='333')
        CaregiverAddress.objects.create(caregiver_fk=first_caregiver,address_fk=address)

        caregiver_address_test =Caregiver.objects.filter(caregiveraddress__address_fk__address_line_1='one drive').first()

        self.assertEqual(first_caregiver,caregiver_address_test)

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

        CaregiverName.objects.create(caregiver_fk=first_caregiver, name_fk=first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now())

        CaregiverName.objects.create(caregiver_fk=second_caregiver, name_fk=second_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now())

        #Create address
        address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=first_caregiver, address_fk=address)

        address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        CaregiverAddress.objects.create(caregiver_fk=second_caregiver, address_fk=address2)


    def test_caregiver_information_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/P7000')
        self.assertTemplateUsed(response,'dataview/caregiver_info.html')

    def test_caregiver_info_page_contains_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response,'P7000')

    def test_other_caregiver_info_page_contains_other_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7001')
        self.assertNotContains(response,'P7000')
        self.assertContains(response,'P7001')

    def test_caregiver_information_page_contains_birthday(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, 'July 3, 1985')

    def test_caregiver_information_page_contains_ewcp(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '0000')

    def test_caregiver_information_page_contains_participation_id(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '01')

    def test_caregiver_information_page_contains_echo_pin(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '333')

    def test_caregiver_information_page_contains_specimen_id(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '4444')

    def test_caregiver_information_page_contains_name(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')

    def test_caregiver_information_page_contains_address(self):
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, 'One Drive')
