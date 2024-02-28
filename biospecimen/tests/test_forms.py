import logging
import unittest

# from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS

from biospecimen.forms import ValidationError
from django.test import TestCase
from django.utils import timezone

from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm,CollectedBiospecimenForm, InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm,CollectedBiospecimenHairSalivaForm,\
ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,DeclinedForm,ReceivedatWSUForm,\
    InitialBioFormPeriNatal,ShippedtoWSUFormPlacenta,ShippedtoMSUForm,ReceivedatMSUForm,ShippedtoWSUFormBlood,ReceivedatWSUBloodForm,ShippedtoEchoBloodForm
from biospecimen.models import Caregiver, CaregiverBiospecimen
from biospecimen.tests.test_views.test_views_caregiver import CaregiverEcho2BiospecimenPageBlood as BL
from biospecimen.tests.db_setup import DatabaseSetup
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

class IncentiveFormTest(TestCase):

    def test_form_renders_incentive_text_input_incentive(self):
        form = IncentiveForm()
        self.assertIn('Incentive',form.as_p())

    @unittest.skip
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

    def test_child_bio_initial_form_postnatal_has_drop_down_with_collected(self):
        form = InitialBioFormPostNatal()
        self.assertIn('Kit Sent',form.as_p())

    def test_bio_initial_form_has_drop_down_with_collected(self):
        form = InitialBioForm()
        self.assertIn('Collected',form.as_p())

    def test_bio_initial_form_perinatal_has_drop_down_with_collected(self):
        form = InitialBioFormPeriNatal()
        self.assertIn('No Consent',form.as_p())
        self.assertNotIn('Declined',form.as_p())

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

    def test_shipped_to_wsu_form_placenta(self):
        form =ShippedtoWSUFormPlacenta()
        self.assertNotIn('tubes',form.as_p())

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

class ReceivedatWSUFormTest(TestCase):

    def test_declined_form_has_declined_date(self):
        form = ReceivedatWSUForm()
        self.assertIn('Received date time', form.as_p())

    def test_declined_form_has_declined_date(self):
        form = ReceivedatWSUForm()
        self.assertIn('Number of tubes', form.as_p())

class ShippedtoMSUFormTest(TestCase):

    def test_declined_form_has_declined_date(self):
        form = ShippedtoMSUForm()
        self.assertIn('Shipped date time', form.as_p())

class ReceivedatMSUFormTest(TestCase):

    def test_declined_form_has_declined_date(self):
        form = ReceivedatMSUForm()
        self.assertIn('Received date time', form.as_p())

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

class CaregiverBloodShippedtoWSUFormTest(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def blood_initial_send_form(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected": c_n_or_x,
                                          })
        return response

    def blood_collected_form_send(self, primary_key, type_of_blood, false_or_true):
        if false_or_true:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/', data={f'blood_form-{type_of_blood}': false_or_true,
                                                                                              f'blood_form-{type_of_blood}_number_of_tubes': 5,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               })
        else:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/', data={f'blood_form-{type_of_blood}': false_or_true,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               })
        return response

    def blood_incentive_form_send(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })

        return response

    def blood_shipped_to_wsu(self, primary_key, type_of_blood, false_or_true, number_of_tubes=5):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5,
                                                                                                         5, 5),
                                          'shipped_to_wsu_form-tracking_number': 555,
                                          f'shipped_to_wsu_form-{type_of_blood}': false_or_true,
                                          f'shipped_to_wsu_form-{type_of_blood}_number_of_tubes': number_of_tubes,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                              2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def blood_received_at_wsu(self,primary_key,type_of_blood,false_or_true,number_of_tubes=5):
        if false_or_true:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                        data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                              f'received_at_wsu_form-{type_of_blood}':type_of_blood,
                                              f'received_at_wsu_form-{type_of_blood}_number_of_tubes': number_of_tubes})
        else:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                        data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    def test_caregiver_blood_shipped_to_wsu_form_fails_if_component_doesnt_match(self):
        primary_key = self.return_caregiver_bio_pk(charm_id='4100', collection_type='B', trimester='S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        logging.debug(f'{primary_key}')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',True)
        self.blood_incentive_form_send(primary_key)
        form = ShippedtoWSUFormBlood(caregiver_bio=caregiver_bio,data={'shipped_date_and_time': timezone.datetime(2023, 12, 5, 5,
                                                       5, 5),
                                          'tracking_number': 555,
                                          f'serum': True,
                                          f'serum_number_of_tubes': 3,
                                          'logged_date_time': timezone.datetime(
                                              2023, 12, 5, 5, 5, 5),
                                          'courier': 'F'})
        #the context manager with self.assertRaises(ValidationError) didn't work probably due to custom error message
        self.assertTrue(form.has_error(NON_FIELD_ERRORS,'ValidationError'))

    def test_caregiver_blood_received_at_wsu_form_fails_if_doesnt_match(self):
        primary_key = self.return_caregiver_bio_pk(charm_id='4100', collection_type='B', trimester='S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        logging.debug(f'{primary_key}')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'serum', True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key,'serum',True)
        form = ReceivedatWSUBloodForm(caregiver_bio=caregiver_bio,
                                     data={'received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                              f'serum':True,
                                              f'serum_number_of_tubes': 3})
        # the context manager with self.assertRaises(ValidationError) didn't work probably due to custom error message
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, 'ValidationError'))

    def test_caregiver_blood_received_at_wsu_form_fails_if_doesnt_match(self):
        primary_key = self.return_caregiver_bio_pk(charm_id='4100', collection_type='B', trimester='S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        logging.debug(f'{primary_key}')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'serum', True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key, 'serum', True)
        self.blood_received_at_wsu(primary_key,'serum',True)
        # the context manager with self.assertRaises(ValidationError) didn't work probably due to custom error message
        form = ShippedtoEchoBloodForm(caregiver_bio=caregiver_bio,
                                      data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5,
                                                                                                          5, 5),
                                          f'serum': True,
                                          f'serum_number_of_tubes': 3})

        self.assertTrue(form.has_error(NON_FIELD_ERRORS, 'ValidationError'))

