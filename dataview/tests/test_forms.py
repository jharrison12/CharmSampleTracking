from django.test import TestCase
from dataview.forms import CaregiverBiospecimenForm, IncentiveForm
import datetime

class CaregiverBioFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CaregiverBiospecimenForm()
        self.assertIn('Collection', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = CaregiverBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['collection_fk'][0])

class IncentiveFormTest(TestCase):

    def test_form_renders_incentive_text_input(self):
        form = IncentiveForm()
        self.assertIn('Incentive',form.as_p())

    def test_incentive_form_validation_for_blank_items(self):
        form = IncentiveForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['incentive_type_fk'][0])