from django.test import TestCase
from dataview.forms import CaregiverBiospecimenForm

class CaregiverBioFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CaregiverBiospecimenForm()
        self.assertIn('Urine 1', form.as_p())