import logging
import sqlite3
import unittest
from django.test import TestCase
from dataview.models import Caregiver, Name, CaregiverName, Address, \
    CaregiverAddress, Email, CaregiverEmail, CaregiverPhone, Phone, SocialMedia, CaregiverSocialMedia, \
    CaregiverPersonalContact, \
    Project, Survey, SurveyOutcome, CaregiverSurvey, Incentive, IncentiveType, \
    Mother, Relation, ConsentItem, \
    NonPrimaryCaregiver, ConsentType, Child, PrimaryCaregiver, HealthcareFacility, Recruitment, ChildName, ChildAddress, \
    ChildSurvey, \
    Assent, ChildAssent, AgeCategory, Race, Ethnicity, Pregnancy, CaregiverChildRelation
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen, Processed, Stored, \
    ShippedWSU, ShippedECHO, \
    Collected
import datetime
from django.utils import timezone
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm, ProcessedBiospecimenForm, StoredBiospecimenForm, \
    ShippedBiospecimenForm, ReceivedBiospecimenForm, CollectedBiospecimenUrineForm, InitialBioForm, ShippedChoiceForm, \
    ShippedtoWSUForm, \
    ShippedtoEchoForm
from django.utils.html import escape
from dataview.tests.db_setup import DatabaseSetup
from django.template.loader import render_to_string


class BiospecimenHistoryPage(DatabaseSetup):

    def test_biospecimen_history_page_returns_correct_template(self):
        response = self.client.get(f'/biospecimen/history/')
        self.assertTemplateUsed(response, 'biospecimen/biospecimen_history.html')

    def test_biospecimen_history_contains_P7000(self):
        response = self.client.get(f'/biospecimen/history/')
        self.assertContains(response, 'P7000')


class BiospecimenEntryHomePage(DatabaseSetup):

    def test_biospecimen_entry_home_page_returns_correct_template(self):
        response = self.client.get(f'/biospecimen/entry/')
        self.assertTemplateUsed(response, 'biospecimen/biospecimen_entry.html')


@unittest.skip
class CaregiverBiospecimenPageTest(DatabaseSetup):

    def get_biospecimen_page(self, biospecimen_id):
        response = self.client.get(f'/biospecimen/caregiver/{biospecimen_id}/')
        return response

    def test_caregiver_biospecimen_page_returns_correct_template(self):
        self.assertTemplateUsed(self.get_biospecimen_page('P7000'), 'biospecimen/caregiver_biospecimen.html')

    def test_caregiver_biospecimen_page_contains_urine_1(self):
        self.assertContains(self.get_biospecimen_page('P7000'), 'Serum 1: Completed')

    def test_caregiver_b_biospecimen_does_not_appear_in_caregiver_a_page(self):
        self.assertNotContains(self.get_biospecimen_page('P7001'), 'Serum 1: Completed')

    def test_caregiver_a_bio_page_shows_all_urines(self):
        self.assertContains(self.get_biospecimen_page('P7000'), "Urine 1")
        self.assertContains(self.get_biospecimen_page('P7000'), "Urine EC")

    def test_caregiver_a_bio_page_shows_hair(self):
        self.assertContains(self.get_biospecimen_page('P7000'), "Prenatal Hair: Completed")

    def test_caregiver_a_bio_page_shows_toenails(self):
        self.assertContains(self.get_biospecimen_page('P7000'), "Prenatal Toenail: Completed")

    def test_caregiver_a_bio_page_shows_saliva(self):
        self.assertContains(self.get_biospecimen_page('P7000'), "Saliva: Completed")

    def test_caregiver_a_bio_page_does_not_show_none_saliva(self):
        self.assertNotContains(self.get_biospecimen_page('P7000'), "None Saliva")

    def test_caregiver_a_bio_page_does_not_show_none_placenta(self):
        self.assertNotContains(self.get_biospecimen_page('P7000'), "None Placenta")

    def test_caregiver_a_bio_page_shows_placenta(self):
        self.assertContains(self.get_biospecimen_page('P7000'), "Placenta: Completed")


@unittest.skip
class CaregiverBioSpecimenEntryPage(DatabaseSetup):

    def get_biospecimen_entry_page(self, biospecimen_id):
        response = self.client.get(f'/biospecimen/caregiver/{biospecimen_id}/entry/')
        return response

    def test_using_correct_template(self):
        self.assertTemplateUsed(self.get_biospecimen_entry_page('P7000'),
                                'biospecimen/caregiver_biospecimen_entry.html')

    def test_caregiver_bio_entry_page_uses_bio_form(self):
        self.assertIsInstance(self.get_biospecimen_entry_page('P7000').context['bio_form'], CaregiverBiospecimenForm)

    def test_bio_entry_redirects_after_post(self):
        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/',
                                    data={'bio_form-collection_fk': self.placenta_two.pk,
                                          'bio_form-status_fk': self.collected.pk,
                                          'bio_form-biospecimen_date': datetime.date(2023, 8, 23),
                                          # 'incentive_fk':  self.incentive_one.pk,
                                          'bio_form-caregiver_fk': self.first_caregiver.pk,
                                          'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                          'incentive_form-incentive_date': datetime.date(2023, 8, 23),
                                          'incentive_form-incentive_amount': 1,
                                          })

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/")

    def test_unique_validation_errors_are_sent_back_to_entry_page(self):
        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/',
                                    data={'bio_form-collection_fk': self.placenta.pk,
                                          'bio_form-status_fk': self.collected.pk,
                                          'bio_form-biospecimen_date': datetime.date(2023, 8, 23),
                                          'bio_form-caregiver_fk': self.first_caregiver.pk,
                                          'incentive_fk': self.incentive_one.pk,
                                          'caregiver_fk': self.first_caregiver.pk,
                                          'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                          'incentive_form-incentive_date': datetime.date(
                                              2023, 8, 23),
                                          'incentive_form-incentive_amount': 1,
                                          })
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')
        expected_error = escape("This type of biospecimen for this charm id already exists")
        self.assertContains(response, expected_error)

    def test_caregiver_bio_entry_page_uses_incentive_form(self):
        self.assertIsInstance(self.get_biospecimen_entry_page('P7000').context['incentive_form'], IncentiveForm)

    def test_bio_entry_is_connected_to_incentive_submitted_in_form(self):
        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/',
                                    data={'bio_form-collection_fk': self.placenta_two.pk,
                                          'bio_form-status_fk': self.collected.pk,
                                          'bio_form-biospecimen_date': datetime.date(2023, 8, 23),
                                          # 'incentive_fk':  self.incentive_one.pk,
                                          'bio_form-caregiver_fk': self.first_caregiver.pk,
                                          'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                          'incentive_form-incentive_date': datetime.date(2023, 8, 23),
                                          'incentive_form-incentive_amount': 1,
                                          })

        placenta_two = CaregiverBiospecimen.objects.filter(collection_fk__collection_type="Placenta").filter(
            collection_fk__collection_number=2).first()

        correct_incentive = Incentive.objects.filter(incentive_amount=1).first()

        self.assertEqual(placenta_two.incentive_fk, correct_incentive)


class ChildBiospecimenPage(DatabaseSetup):

    def test_child_biospecimen_page_uses_correct_template(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertTemplateUsed(response, 'biospecimen/child_biospecimen.html')

    def test_child_biospecimen_page_has_header(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertContains(response, 'Child ID: 7000M1')

    @unittest.skip
    def test_child_biospecimen_page_has_urine(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertContains(response, 'Urine 6: Completed')

    def test_child_biospecimen_contains_all_child_biospecimens(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        child_bios = ChildBiospecimen.objects.values('collection_fk__collection_type_fk__collection_type')
        child_bios_list = list(set(value for dic in child_bios for value in dic.values()))
        for value in child_bios_list:
            self.assertContains(response, value)


class CaregiverSingleBiospecimenHistoryPage(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, collection_num, trimester=None, project='ECHO1'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        if trimester is not None:
            caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                            collection_fk__collection_type_fk__collection_type=collection_type,
                                                            trimester_fk__trimester=trimester,
                                                            project_fk__project_name=project)
        else:
            caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                            collection_fk__collection_type_fk__collection_type=collection_type,
                                                            collection_fk__collection_number_fk__collection_number=collection_num,
                                                            project_fk__project_name=project)

        return caregiverbio.pk

    def test_caregiver_blood_spot_page_uses_correct_template(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_history.html')

    def test_caregiver_blood_spot_contains_blood_spot_id(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        logging.debug(response.content)
        self.assertContains(response, 'ID: 1111BS')

    def test_caregiver_blood_spot_page_uses_processed_form_if_no_processed_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7001')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.debug(f"processed is {processed_one.count()}")
        self.assertIsInstance(response.context['processed_form'], ProcessedBiospecimenForm)

    def test_caregiver_blood_spot_page_does_not_show_processed_form_if_processed_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7000')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.debug(f"processed is {processed_one.count()}")
        self.assertNotContains(response, '<form>', html=True)

    def test_caregiver_bio_iem_shows_processed_form_if_no_processed_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        self.assertIsInstance(response.context['processed_form'], ProcessedBiospecimenForm)

    def test_caregiver_blood_spot_page_uses_stored_form_if_processed_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7000')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.debug(f"processed is {processed_one.count()}")
        self.assertIsInstance(response.context['stored_form'], StoredBiospecimenForm)

    def test_caregiver_blood_spot_page_uses_shipped_form_if_stored_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7003', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7003/{caregiver_bio_pk}/history/')
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7003')
        stored_one = Stored.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                           status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.debug(f"stored is {stored_one.count()}")
        self.assertIsInstance(response.context['shipped_form'], ShippedBiospecimenForm)

    def test_caregiver_blood_spot_page_shows_shipped_data_if_completed(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        self.assertContains(response, 'Courier:Fedex')

    def test_caregiver_bloodspot_page_uses_received_form_if_shipped_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7004', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7004/{caregiver_bio_pk}/history/')
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7004')
        shipped_one = Stored.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                            status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.debug(f"shipped is {shipped_one.count()}")
        self.assertIsInstance(response.context['received_form'], ReceivedBiospecimenForm)

    def test_caregiver_blood_spot_page_shows_received_data_if_completed(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        logging.debug(f"recieved?{response.content}")
        self.assertContains(response, 'Quantity:19')

    def test_blood_plams_page_uses_correct_template(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Plasma',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_history.html')


class CaregiverEcho2BiospecimenPageNonBlood(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def test_echo2_initial_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    def test_echo2_bio_page_shows_caregiver_id(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'P7000')

    def test_echo2_bio_page_shows_trimester_if_urine(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Trimester: First')

    def test_echo2_bio_page_shows_initial_collected_or_not_form_if_no_collected_object_and_collection_urine(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioForm)

    @unittest.skip
    def test_echo2_bio_page_does_not_show_collected_urine_form_if_no_collected_object_and_collection_urine(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertNotIsInstance(response.context['collected_form'], CollectedBiospecimenUrineForm)

    def test_echo2_bio_page_does_not_show_formalin_if_urine(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertNotContains(response, 'formalin')

    def test_echo2_bio_entry_urine_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={"id_urine_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "id_urine_form-processed_date_time": timezone.datetime(
                                              2023, 5, 5, 5, 5,
                                              5),
                                          "id_urine_form-stored_date_time": timezone.datetime(
                                              2023, 5, 5, 5, 5,
                                              5),
                                          "id_urine_form-number_of_tubes": 5
                                          })

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_initial_posts_to_initial_post_view(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected': ['C']})
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_entry_shipped_choice_redirects_after_post_wsu(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo': ['W']})

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_entry_shipped_choice_redirects_after_post_echo(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo': ['E']})

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_page_shows_shipped_choice_form_if_collected_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_bio_page_shows_shipped_choice_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'T')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        status_item = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        new_ship_to_wsu = ShippedWSU()
        status_item.shipped_wsu_fk = new_ship_to_wsu
        new_ship_to_wsu.save()
        caregiver_bio.save()
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUForm)

    def test_echo2_bio_page_shows_shipped_to_wsu_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('P7001', 'Urine', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        status_item = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Courier: FedEx')

    def test_echo2_bio_page_shows_shipped_to_echo_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('P7001', 'Urine', 'T')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        status_item = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        response = self.client.get(f'/biospecimen/caregiver/P7001/{primary_key}/entry/')
        # logging.debug(response.content.decode())
        # print html RESPONSE CONTENT DECODE
        self.assertContains(response, 'Shipped Date Time:')

    def test_echo2_bio_page_shows_shipped_echo_form_if_echo_fk_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'T')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        status_item = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        new_ship_to_echo = ShippedECHO()
        status_item.shipped_echo_fk = new_ship_to_echo
        new_ship_to_echo.save()
        status_item.save()
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        logging.debug(f"shipped to echo {response.context}")
        self.assertIsInstance(response.context['shipped_echo_form'], ShippedtoEchoForm)

    def test_echo2_bio_entry_shipped_echo_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7001', 'Urine', 'S')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_echo/post/',
                                    data={'shipped_date_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")


class CaregiverEcho2BiospecimenPageBlood(DatabaseSetup):
    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def add_collected_fk_to_biospecimen(self, biospecimen_pk):
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=biospecimen_pk)
        new_status = Status()
        caregiver_bio.status_fk = new_status
        new_status.save()
        caregiver_bio.save()
        collected = Collected()
        new_status.collected_fk = collected
        collected.save()
        new_status.save()

    def test_echo2_initial_bio_blood_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_bio_page_shows_trimester_if_blood(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Trimester: First')

    def test_echo2_bio_page_shows_collected_blood_form_if_blood_and_collected(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        logging.debug(f"{response.content.decode()}")
        self.assertContains(response, '<input type="checkbox" name="blood_form-serum')
        self.assertContains(response, '<input type="checkbox" name="blood_form-whole_blood')
        self.assertContains(response, '<input type="checkbox" name="blood_form-plasma')
        self.assertContains(response, '<input type="checkbox" name="blood_form-buffy_coat')
        self.assertContains(response, '<input type="checkbox" name="blood_form-red_blood_cells')

    def test_echo2_bio_entry_blood_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={"id_blood_form-serum": True,
                                          })

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_entry_blood_updates_serum_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-serum': True,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Serum', 'F')
        serum = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertEqual(serum.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(serum.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(serum.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(serum.status_fk.collected_fk.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_plasma_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-plasma': True,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Plasma', 'F')
        plasma = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertEqual(plasma.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(plasma.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(plasma.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(plasma.status_fk.collected_fk.number_of_tubes,5)


    def test_echo2_bio_entry_blood_updates_whole_blood_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-whole_blood': True,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertEqual(whole_blood.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(whole_blood.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(whole_blood.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(whole_blood.status_fk.collected_fk.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_buffy_coat_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-buffy_coat': True,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Buffy Coat', 'F')
        buffy_coat = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertEqual(buffy_coat.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(buffy_coat.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(buffy_coat.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(buffy_coat.status_fk.collected_fk.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_red_blood_count_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={'blood_form-red_blood_cells': True,
                                          'blood_form-collected_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-processed_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-stored_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')
        red_blood_count = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertEqual(red_blood_count.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(red_blood_count.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(red_blood_count.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertEqual(red_blood_count.status_fk.collected_fk.number_of_tubes, 5)


    def test_echo2_bio_entry_blood_does_not_create_red_blood_count_if_checkbox_not_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={'blood_form-red_blood_cells': False,
                                          'blood_form-collected_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-processed_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-stored_date_time': timezone.datetime(
                                              2023, 5, 5, 5, 5, 5),
                                          'blood_form-number_of_tubes': 5})
        with self.assertRaises(CaregiverBiospecimen.DoesNotExist):
            primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')


    def test_echo2_bio_entry_blood_does_not_update_whole_blood_if_checkbox_not_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-whole_blood': False,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertNotEqual(whole_blood.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.number_of_tubes,5)

    def test_echo2_bio_entry_blood_shows_updated_values_if_posted(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={'blood_form-buffy_coat': True,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response,'Number of Tubes: 5')

    def test_echo2_bio_entry_whole_blood_is_checked_and_not_editable(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, '<input type="checkbox" name="blood_form-whole_blood" disabled id="id_blood_form-whole_blood" checked>')

