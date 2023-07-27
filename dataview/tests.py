from django.test import TestCase
from dataview.models import Caregiver

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')

class CaregiverModelsTest(TestCase):

    def test_saving_and_retrieving_caregiver(self):
        caregiver_one = Caregiver()
        caregiver_one.save()

        caregiver_one.charm_project_identifier = 'P7000'
        caregiver_one.save()

        saved_caregiver = Caregiver.objects.first()
        self.assertEqual(saved_caregiver,caregiver_one)

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
