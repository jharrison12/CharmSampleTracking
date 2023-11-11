from django.test import TestCase
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm,ReceivedBiospecimenForm,CollectedBiospecimenForm, InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,InitialBioFormChild,KitSentForm,CollectedChildUrineStoolForm,CollectedBiospecimenHairSalivaForm,\
ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,DeclinedForm
import datetime

class CaregiverBioFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CaregiverBiospecimenForm()
        self.assertIn('Collection', form.as_p())

    def test_form_validation_for_blank_items_caregiver_bio(self):
        form = CaregiverBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['collection_fk'][0])

class ProcessedBioFormTest(TestCase):

    def test_form_renders_proccessed_for_input(self):
        form = ProcessedBiospecimenForm()
        self.assertIn('Processed', form.as_p())

    def test_form_validation_for_blank_items_processed(self):
        form = ProcessedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class StoredBioFormTest(TestCase):

    def test_form_renders_stored_for_input(self):
        form = StoredBiospecimenForm()
        self.assertIn('Stored', form.as_p())

    def test_form_validation_for_blank_items_stored(self):
        form = StoredBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class ShippedBioFormTest(TestCase):
    def test_form_renders_shipped_for_input_shipped(self):
        form = ShippedBiospecimenForm()
        self.assertIn('Shipped', form.as_p())

    def test_form_validation_for_blank_items_shipped(self):
        form = ShippedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class ReceivedBioFormTest(TestCase):
    def test_form_renders_shipped_for_input_received(self):
        form = ReceivedBiospecimenForm()
        self.assertIn('Received', form.as_p())

    def test_form_validation_for_blank_items_received(self):
        form = ReceivedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['outcome_fk'][0])

class IncentiveFormTest(TestCase):

    def test_form_renders_incentive_text_input_incentive(self):
        form = IncentiveForm()
        self.assertIn('Incentive',form.as_p())

    def test_incentive_form_validation_for_blank_items_incentive(self):
        form = IncentiveForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['incentive_type_fk'][0])

class KitSentFormTest(TestCase):
    def test_form_renders_date_kit_sent_text_input(self):
        form = KitSentForm()
        self.assertIn('Kit sent date',form.as_p())

class CollectedChildUrineStoolFormTest(TestCase):

    def test_form_renders_date_collected_child_urine_text_input(self):
        form = CollectedChildUrineStoolForm()
        self.assertIn('Number of tubes',form.as_p())

class CollectedChildBloodSpotFormTest(TestCase):

    def test_form_collected_does_not_contain_number_of_tubes(self):
        form = CollectedChildBloodSpotForm()
        self.assertNotIn('Number of tubes',form.as_p())

    def test_form_collected_does_contain_number_of_cards(self):
        form = CollectedChildBloodSpotForm()
        self.assertIn('Number of cards',form.as_p())

class ShippedtoWSUChildFormTest(TestCase):

    def test_form_shipped_wsudoes_not_contain_number_of_tubes(self):
        form = ShippedtoWSUFormChild()
        self.assertNotIn('Number of tubes',form.as_p())

    def test_form_shipped_wsu_child_does_contain_number_of_cards(self):
        form = ShippedtoWSUFormChild()
        self.assertNotIn('Number of cards',form.as_p())

class CollectedChildBloodSpotOneYearFormTest(TestCase):

    def test_form_collected_child_blood_does_not_contain_number_of_tubes(self):
        form = CollectedChildBloodSpotHairFormOneYear()
        print(type(form))
        self.assertNotIn('Number of tubes',form.as_p())

    def test_form_collected_child_blood_does_contain_number_of_cards(self):
        form = CollectedChildBloodSpotHairFormOneYear()
        self.assertNotIn('Number of cards',form.as_p())

class CaregiverCollectedFormTest(TestCase):

    def test_collected_bio_form_renders_collected_text_input(self):
        form = CollectedBiospecimenForm()
        self.assertIn('Collected',form.as_p())

    def test_collected_form_validation_for_blank_items(self):
        form = CollectedBiospecimenForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['collected_date_time'][0])

class CaregiverCollectedSalivaHairFormTest(TestCase):

    def test_collected_bio_hairform_renders_collected_text_input(self):
        form = CollectedBiospecimenHairSalivaForm()
        self.assertIn('Date collected',form.as_p())

    def test_collected_bio_hairform_validation_for_blank_items(self):
        form = CollectedBiospecimenHairSalivaForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['date_collected'][0])

class CaregiverShippedChoiceHairSaliva(TestCase):

    def test_bio_shipped_chioce_form_echo_does_not_have_shipped_to_wsu(self):
        form = ShippedChoiceEchoForm()
        self.assertNotIn('Shipped to WSU',form.as_p())

class CaregiverBioInitialStatusForm(TestCase):

    def test_child_bio_initial_form_has_drop_down_with_collected(self):
        form = InitialBioFormChild()
        self.assertIn('Kit Sent',form.as_p())

class CaregiverBioInitialStatusForm(TestCase):

    def test_bio_initial_form_has_drop_down_with_collected(self):
        form = InitialBioForm()
        self.assertIn('Collected',form.as_p())

class CaregiverBioShippedChoiceForm(TestCase):

    def test_bio_shipped_choice_form_has_shipped_to_wsu(self):
        form = ShippedChoiceForm()
        self.assertIn('Shipped to WSU',form.as_p())


class CaregiverShippedtoWSUForm(TestCase):

    def test_bio_shipped_wsu_form_has_shipped_to_wsu(self):
        form = ShippedtoWSUForm()
        self.assertIn('Shipped date and time:',form.as_p())

    def test_shipped_to_wsu_form_validation_for_blank_items(self):
        form = ShippedtoWSUForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['shipped_date_and_time'][0])

class CaregiverShippedtoECHOForm(TestCase):

    def test_bio_shipped_echo_form_has_shipped_datetime(self):
        form = ShippedtoEchoForm()
        self.assertIn('Shipped date and time:',form.as_p())

    def test_shipped_to_echo_form_validation_for_blank_items(self):
        form = ShippedtoEchoForm(data={'':''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required',form.errors['shipped_date_and_time'][0])

class DeclinedFormTest(TestCase):

    def test_declined_form_has_declined_date(self):
        form = DeclinedForm()
        self.assertIn('Declined date', form.as_p())

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
        self.assertIn('<input type="checkbox" name="red_blood_cells',form.as_p())

    def test_blood_collected_form_has_checkbox_for_serum(self):
        form = CollectedBloodForm()
        self.assertIn('<input type="checkbox" name="serum', form.as_p())
