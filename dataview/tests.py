from django.test import TestCase
from dataview.models import Caregiver
import datetime

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

    def test_caregiver_information_page_uses_correct_template(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        response = self.client.get('/data/caregiver/P7000')
        self.assertTemplateUsed(response,'dataview/caregiver_info.html')

    def test_caregiver_info_page_contains_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response,'P7000')

    def test_other_caregiver_info_page_contains_other_caregiver_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000')
        Caregiver.objects.create(charm_project_identifier='P7001')
        response = self.client.get(f'/data/caregiver/P7001')
        self.assertNotContains(response,'P7000')
        self.assertContains(response,'P7001')

    def test_caregiver_information_page_contains_birthday(self):
        Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3))
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, 'July 3, 1985')

    def test_caregiver_information_page_contains_ewcp(self):
        Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000')
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '0000')

    def test_caregiver_information_page_contains_participation_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000',date_of_birth=datetime.date(1985,7,3),ewcp_participant_identifier='0000', participation_level_identifier='01')
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '01')

    def test_caregiver_information_page_contains_participation_id(self):
        Caregiver.objects.create(charm_project_identifier='P7000',echo_pin='333')
        response = self.client.get(f'/data/caregiver/P7000')
        self.assertContains(response, '333')
