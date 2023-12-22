import logging
import unittest
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen,\
    ShippedECHO, Collected, Caregiver, Project, Child,User
import datetime
from django.utils import timezone
from biospecimen.forms import IncentiveForm, ProcessedBiospecimenForm, StoredBiospecimenForm, \
    ShippedBiospecimenForm, ReceivedBiospecimenForm, CollectedBiospecimenUrineForm, InitialBioForm, ShippedChoiceForm, \
    ShippedtoWSUForm, ShippedtoEchoForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm, \
    ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,InitialBioFormChildTooth,\
    CollectedChildToothForm,DeclinedForm,ReceivedatWSUForm,ShippedtoMSUForm
from biospecimen.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)


class ChildBiospecimenPage(DatabaseSetup):

    def send_kit(self,primary_key,kit_sent):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={"initial_bio_form-collected_not_collected_kit_sent": f'{kit_sent}',
                                          "initial_bio_form_button": ['Submit']
                                          })
        return response

    def send_kit_form(self,primary_key,bio_id):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={"kit_sent_form-kit_sent_date": '2023-09-03',
                                          'kit_sent_form-echo_biospecimen_id': bio_id,
                                          'kit_sent_form_button':['Submit']
                                          })
        return response

    def send_collected_form(self,primary_key,collection_type):
        if collection_type in ('U','O'):
            response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                        data={"collected_child_form-in_person_remote": 'I',
                                              "collected_child_form-date_received":'2023-09-03',
                                              "collected_child_form-number_of_tubes":'4',
                                              "collected_form_button": ['Submit']
                                              })
        elif collection_type==('D'):
            response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                        data={"collected_child_form-in_person_remote": 'I',
                                              "collected_child_form-date_received":'2023-09-03',
                                              "collected_child_form-number_of_cards":'4',
                                              "collected_form_button": ['Submit']
                                              })
        elif collection_type==('E'):
            response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                        data={"collected_child_form-date_collected":'2023-09-03',
                                              "collected_form_button": ['Submit']})
        return response

    def send_incentive_form(self,primary_key):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={'child_incentive_form-incentive_date': ['2023-09-03'],
                                          'incentive_form_button': ['Submit']})
        logging.debug(response.content)
        return response

    def send_wsu_or_echo(self,primary_key,e_or_w):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={'child_shipped_choice_form-shipped_to_wsu_or_echo': [f'{e_or_w}'],
                                          'shipped_choice_form_button': ['Submit']})
        return response

    def send_to_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={'child_shipped_to_wsu_form-shipped_date_and_time': ['2023-09-27 12:52:26'],
                                          'shipped_to_wsu_form_button': ['Submit']})
        return response

    def received_at_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/child/4100F1/{primary_key}/initial/',
                                    data={'child_received_at_wsu_form-received_date_time': ['2023-09-27 12:52:26'],
                                          'received_at_wsu_form_button': ['Submit']})
        return response

    def return_child_bio_pk(self,child_id,collection_type,age):
        child_object = Child.objects.get(charm_project_identifier=child_id)
        logging.debug(f"{child_object}")
        child_biospecimen = ChildBiospecimen.objects.get(child_fk=child_object,
                                                         collection_fk__collection_type=collection_type,
                                                         age_category_fk__age_category=age)

        return child_biospecimen.pk

    def test_echo2_initial_child_returns_correct_template(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/child_biospecimen_initial.html')

    def test_echo2_initial_child_urine_shows_urine(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertContains(response,'Urine')

    def test_echo2_initial_child_urine_shows_correct_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormPostNatal)

    def test_echo2_initial_child_tooth_shows_correct_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormChildTooth)

    def test_echo2_initial_child_urine_redirects_after_post_kit_sent(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_post_not_collected(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'N')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_no_declined(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'X')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_declined_if_declined(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'X')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertContains(response,'Declined')

    def test_echo2_initial_child_urine_shows_declined_form_if_declined(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'X')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['declined_form'], DeclinedForm)

    def test_echo2_initial_child_urine_shows_kit_sent_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'K')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_initial_child_tooth_shows_kit_sent_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST')
        response = self.send_kit(primary_key,'K')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_initial_child_urine_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildUrineStoolForm)

    def test_echo2_initial_kit_sent_form_assigns_bio_id_child_bio(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        child_bio = ChildBiospecimen.objects.get(pk=primary_key)
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        child_bio = ChildBiospecimen.objects.get(pk=primary_key)
        self.assertEqual(child_bio.biospecimen_id,'5555555')

    def test_echo2_initial_child_bloodspots_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'ZF')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildBloodSpotForm)

    def test_echo2_initial_child_tooth_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'E', 'ST')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildToothForm)


    def test_echo2_initial_child_bloodspots_12_to_13_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'TT')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildBloodSpotHairFormOneYear)

    def test_echo2_initial_child_bloodspots_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_bloodspots_12_to_13_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'TT')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_bloodspots_redirects_after_collected_form_submitted(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'D')
        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_collected_form_submitted(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')


    def test_echo2_initial_child_urine_shows_incentive_form_after_collection_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_initial_child_bloodspots_12_months_shows_echo_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'S', 'TT')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        self.send_collected_form(primary_key,'D')
        response = self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertNotContains(response,'Shipped to WSU')

    def test_echo2_initial_child_urine_shows_shipped_to_echo_form_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.send_incentive_form(primary_key)
        response = self.send_to_wsu(primary_key)
        response = self.received_at_wsu(primary_key)
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertIsInstance(response.context['shipped_to_echo_form'], ShippedtoEchoForm)


    def test_echo2_initial_child_urine_shows_shipped_to_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key, 'W')
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        self.assertIsInstance(response.context['shipped_to_wsu_form'], ShippedtoWSUFormChild)
        
    def test_echo2_initial_child_urine_redirects_after_shipped_to_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'W')
        response = self.send_to_wsu(primary_key)
        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_received_at_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key, 'W')
        response = self.send_to_wsu(primary_key)
        response = self.client.get(f'/biospecimen/child/4100F1/{primary_key}/initial/')
        logging.debug(f"response {response.content.decode()}")
        self.assertIsInstance(response.context['received_at_wsu_form'], ReceivedatWSUForm)

    def test_echo2_initial_child_urine_redirects_after_received_at_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('4100F1', 'U', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'U')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'W')
        response = self.send_to_wsu(primary_key)
        response = self.received_at_wsu(primary_key)
        self.assertRedirects(response, f'/biospecimen/child/4100F1/{primary_key}/initial/')

