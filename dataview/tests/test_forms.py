from django.test import TestCase
from dataview.forms import CaregiverBioForm

class CaregiverBioFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CaregiverBioForm()
        self.fail(form.as_p())