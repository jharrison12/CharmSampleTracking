from django.test import TestCase

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')

class CaregiverPageTest(TestCase):
    def test_caregiver_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver')
        self.assertTemplateUsed(response, 'dataview/caregiver.html')

    def test_mother_page_contains_caregiver_id(self):
        pass