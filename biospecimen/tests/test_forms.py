from django.test import TestCase
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm,ReceivedBiospecimenForm,CollectedBiospecimenForm, InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm
import datetime

class CaregiverBioFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CaregiverBiospecimenForm()
        self.assertIn('Collection', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = CaregiverBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['collection_fk'][0])

class ProcessedBioFormTest(TestCase):

    def test_form_renders_proccessed_for_input(self):
        form = ProcessedBiospecimenForm()
        self.assertIn('Processed', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ProcessedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class StoredBioFormTest(TestCase):

    def test_form_renders_proccessed_for_input(self):
        form = StoredBiospecimenForm()
        self.assertIn('Stored', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = StoredBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class ShippedBioFormTest(TestCase):
    def test_form_renders_shipped_for_input(self):
        form = ShippedBiospecimenForm()
        self.assertIn('Shipped', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ShippedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class ReceivedBioFormTest(TestCase):
    def test_form_renders_shipped_for_input(self):
        form = ReceivedBiospecimenForm()
        self.assertIn('Received', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ReceivedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class IncentiveFormTest(TestCase):

    def test_form_renders_incentive_text_input(self):
        form = IncentiveForm()
        self.assertIn('Incentive',form.as_p())

    def test_incentive_form_validation_for_blank_items(self):
        form = IncentiveForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['incentive_type_fk'][0])


class CaregiverCollectedFormTest(TestCase):

    def test_collected_form_renders_collected_text_input(self):
        form = CollectedBiospecimenForm()
        self.assertIn('Collected',form.as_p())

    def test_collected_form_validation_for_blank_items(self):
        form = CollectedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['collected_date_time'][0])

class CaregiverBioInitialStatusForm(TestCase):

    def test_bio_initial_form_has_drop_down_with_collected(self):
        form = InitialBioForm()
        self.assertIn('Collected',form.as_p())

class CaregiverBioShippedChoiceForm(TestCase):

    def test_bio_shipped_chioce_form_has_shipped_to_wsu(self):
        form = ShippedChoiceForm()
        self.assertIn('Shipped to WSU',form.as_p())


class CaregiverShippedtoWSUForm(TestCase):

    def test_bio_shipped_wsu_form_has_shipped_to_wsu(self):
        form = ShippedtoWSUForm()
        self.assertIn('Shipped date and time:',form.as_p())

    def test_collected_form_validation_for_blank_items(self):
        form = ShippedtoWSUForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['shipped_date_and_time'][0])

class CaregiverShippedtoECHOForm(TestCase):

    def test_bio_shipped_echo_form_has_shipped_datetime(self):
        form = ShippedtoEchoForm()
        self.assertIn('Shipped date and time:',form.as_p())

    def test_collected_form_validation_for_blank_items(self):
        form = ShippedtoEchoForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['shipped_date_and_time'][0])

class CaregiverBloodCollectedForm(TestCase):

    def test_blood_collected_form_has_datetime_collected(self):
        form = CollectedBloodForm()
        self.assertIn('Collected date time:', form.as_p())

    def test_blood_collected_form_has_checkbox_for_whole_blood(self):
        form =CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="whole_blood',form.as_p())

    def test_blood_collected_form_has_checkbox_for_plasma(self):
        form =CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="plasma',form.as_p())

    def test_blood_collected_form_has_checkbox_for_buffy_coat(self):
        form =CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="buffy_coat',form.as_p())

    def test_blood_collected_form_has_checkbox_for_rbc(self):
        form =CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="red_blood_count',form.as_p())

    def test_blood_collected_form_has_checkbox_for_serum(self):
        form = CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="serum', form.as_p())
