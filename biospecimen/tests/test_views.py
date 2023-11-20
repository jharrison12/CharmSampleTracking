import logging
import sqlite3
import unittest
from django.test import TestCase
from dataview.models import Caregiver, Project,Incentive,  Child,User
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen, Processed, Stored, \
    ShippedWSU, ShippedECHO, Collected
import datetime
from django.utils import timezone
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm, ProcessedBiospecimenForm, StoredBiospecimenForm, \
    ShippedBiospecimenForm, ReceivedBiospecimenForm, CollectedBiospecimenUrineForm, InitialBioForm, ShippedChoiceForm, \
    ShippedtoWSUForm, ShippedtoEchoForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm, CollectedBiospecimenHairSalivaForm,\
    ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,InitialBioFormChildTooth,\
    CollectedChildToothForm,DeclinedForm,ReceivedatWSUForm
from django.utils.html import escape
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)

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

    def return_processed(self,charm_id):
        bloodspots = Collection.objects.get(collection_type_fk__collection_type='Bloodspots',
                                            collection_number_fk__collection_number='F')
        caregiver = Caregiver.objects.get(charm_project_identifier=f'{charm_id}')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=bloodspots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)
        return processed_one

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
        processed_one = self.return_processed('P7000')
        self.assertIsInstance(response.context['processed_form'], ProcessedBiospecimenForm)

    def test_caregiver_blood_spot_page_does_not_show_processed_form_if_processed_data(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Bloodspots',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        processed_one = self.return_processed('P7000')
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
        processed_one = self.return_processed('P7000')
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
        logging.debug(f"received?{response.content}")
        self.assertContains(response, 'Quantity:19')

    def test_blood_plams_page_uses_correct_template(self):
        caregiver_bio_pk = self.return_caregiver_bio_pk(charm_id='P7000', collection_type='Plasma',
                                                        collection_num='F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{caregiver_bio_pk}/history/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_history.html')

class CaregiverEcho2BiospecimenPageNonBlood(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester,age_category=None, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)
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

    def test_echo2_bio_entry_urine_shows_user_who_is_logged_in_after_submitted(self):
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

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response,'Logged By: testuser')

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

    def test_echo2_bio_entry_shows_incentive_form_if_collected_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'S')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected': ['C']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={"urine_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "urine_form-processed_date_time": timezone.datetime(
                                              2023, 5, 5, 5, 5,
                                              5),
                                          "urine_form-stored_date_time": timezone.datetime(
                                              2023, 5, 5, 5, 5,
                                              5),
                                          "urine_form-number_of_tubes": 5
                                          })

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')

        logging.critical(response.content.decode())

        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_bio_page_shows_shipped_choice_form_if_collected_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_bio_page_shows_wsu_shipped_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Urine', 'T')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        status_item = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        new_ship_to_wsu = ShippedWSU()
        status_item.shipped_wsu_fk = new_ship_to_wsu
        new_ship_to_wsu.shipped_by = User.objects.get(pk=1)
        new_ship_to_wsu.save()
        caregiver_bio.save()
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUForm)

    def test_echo2_bio_page_shows_shipped_to_wsu_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('P7001', 'Urine', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Courier: FedEx')

    def test_echo2_bio_page_shows_shipped_by_user(self):
        primary_key = self.return_caregiver_bio_pk('P7001', 'Urine', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Shipped By: testuser')

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
                                    data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_page_shows_kit_sent_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')
        logging.debug(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/hairandsaliva/')

        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_bio_page_redirects_after_initial_kit_sent_submission(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')
        logging.debug(primary_key)

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        self.assertRedirects(response,f"/biospecimen/caregiver/P7000/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_redirects_after_kit_sent_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')
        logging.debug(primary_key)

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/kit_sent/post/',
                                    data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                                          'echo_biospecimen_id': 3333})

        self.assertRedirects(response,f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_page_hair_saliva_uses_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, age_category='ZF')

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')

        self.assertTemplateUsed(response, "biospecimen/caregiver_biospecimen_initial.html")


    def test_echo2_bio_page_shows_collected_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')
        logging.debug(primary_key)

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/kit_sent/post/',
                                    data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                                          'kit_sent_form-echo_biospecimen_id': 3333})

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')

        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)



    def test_echo2_bio_page_initial_form_shows_denied_not_collected_kit_sent_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')
        logging.debug(primary_key)

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')

        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormPostNatal)


    def test_echo2_bio_page_shows_shipped_echo_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None,age_category='ZF')

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/kit_sent/post/',
                                    data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                                          'kit_sent_form-echo_biospecimen_id': 3333})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={'hair_saliva_form-in_person_remote': 'I',
                                          'hair_saliva_form-date_collected':'2023-09-27',
                                          'hair_saliva_form-incentive_date':'2023-09-27'})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/incentive/post/',
                                    data={'incentive_form-incentive_date': '2023-09-27'})

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')

        logging.critical(response.content.decode())

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceEchoForm)

    def test_echo2_bio_page_incentive_post_redirects(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Hair', trimester=None, age_category='ZF')
        logging.debug(primary_key)

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={'initial_form-collected_not_collected_kit_sent': ['K']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/kit_sent/post/',
                                    data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                                          'kit_sent_form-echo_biospecimen_id': 3333})


        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={'hair_saliva_form-in_person_remote': 'I',
                                          'hair_saliva_form-date_collected': '2023-09-27',
                                          'hair_saliva_form-incentive_date': '2023-09-27'})

        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        logging.critical(f"what {response.content.decode()}")

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/incentive/post/',
                                    data={'incentive_form-incentive_date': '2023-09-27'})

        self.assertRedirects(response,f"/biospecimen/caregiver/P7000/{primary_key}/entry/")


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
        collected = Collected(logged_by=User.objects.get(pk=1))
        new_status.collected_fk = collected
        collected.save()
        new_status.save()
        caregiver_bio.save()


    def add_shipped_echo_to_biospecimen(self, biospecimen_pk):
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=biospecimen_pk)
        new_status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        new_echo = ShippedECHO()
        new_status.shipped_echo_fk = new_echo
        new_echo.save()
        new_status.save()
        caregiver_bio.save()

    def create_bio_specimen(self,caregiver_id,collection_type,project="ECHO2"):
        caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_id)
        collection = Collection.objects.get(collection_type_fk__collection_type=collection_type,collection_number_fk__collection_number=None)
        project = Project.objects.get(project_name=project)
        caregiver_bio = CaregiverBiospecimen()
        new_status = Status()
        caregiver_bio.status_fk = new_status
        caregiver_bio.caregiver_fk = caregiver
        caregiver_bio.collection_fk = collection
        caregiver_bio.project_fk = project
        new_status.save()
        caregiver_bio.save()
        collected = Collected(logged_by=User.objects.get(pk=1))
        new_status.collected_fk = collected
        collected.save()
        new_status.save()
        return caregiver_bio.pk

    def blood_collected_form_send(self, primary_key, type, false_or_true):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/', data={f'blood_form-{type}': false_or_true,
                                                                                               'blood_form-collected_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-processed_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-stored_date_time': timezone.datetime(
                                                                                                   2023, 5, 5, 5, 5, 5),
                                                                                               'blood_form-number_of_tubes': 5})
        return response

    def blood_initial_send_form(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected": c_n_or_x,
                                          })
        return response

    def blood_incentive_form_send(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })

        return response

    def blood_shipped_choice_form_send(self,primary_key,w_or_e):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_choice/post/',
                                    data={"shipped_choice_form-shipped_to_wsu_or_echo": w_or_e,
                                          })

        return response


    def blood_shipped_to_wsu(self,primary_key):
        response =  self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def blood_received_at_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    #Template Tests

    def test_echo2_initial_bio_blood_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_entry_bio_blood_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry_blood.html')
    #move
    def test_echo2_entry_bio_hair_saliva_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/hairsaliva/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    def test_echo2_bio_page_shows_trimester_if_blood(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        self.assertContains(response, 'Trimester: First')


    def test_echo2_bio_page_shows_collected_blood_form_if_blood_and_collected(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.debug(f"{response.content.decode()}")
        self.assertContains(response, '<input type="checkbox" name="blood_form-serum')
        self.assertContains(response, '<input type="checkbox" name="blood_form-whole_blood')
        self.assertContains(response, '<input type="checkbox" name="blood_form-plasma')
        self.assertContains(response, '<input type="checkbox" name="blood_form-buffy_coat')
        self.assertContains(response, '<input type="checkbox" name="blood_form-red_blood_cells')

    def test_echo2_bio_entry_blood_shows_updated_values_if_posted(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={'blood_form-buffy_coat': True,'blood_form-whole_blood':True,
                                          'blood_form-collected_date_time': timezone.datetime( 2023, 5, 5, 5, 5, 5),
                                          'blood_form-processed_date_time': timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          'blood_form-stored_date_time': timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          'blood_form-number_of_tubes': 5})
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertContains(response,'Number of Tubes: 5')

    def test_echo2_bio_entry_whole_blood_is_checked_and_not_editable(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        self.assertContains(response, '<input type="checkbox" name="blood_form-whole_blood" disabled id="id_blood_form-whole_blood" checked>')

    # Redirection tests

    def test_echo2_bio_blood_form_redirects_after_post(self):
        #not sure what this is testing
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.blood_initial_send_form(primary_key, 'C')
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={"id_blood_form-serum": True,
                                          })

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")


    def test_echo2_bio_blood_initial_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        response = self.blood_initial_send_form(primary_key,'C')

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_collected_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key,'C')
        response = self.blood_collected_form_send(primary_key,"serum",True)

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_incentive_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key,'C')
        self.blood_collected_form_send(primary_key,"serum",True)
        response = self.blood_incentive_form_send(primary_key)

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_shipped_choice_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        response = self.blood_shipped_choice_form_send(primary_key,'W')

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_shipped_wsu_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_choice_form_send(primary_key, 'W')
        response = self.blood_shipped_to_wsu(primary_key)

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_shipped_echo_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        response = self.blood_shipped_choice_form_send(primary_key, 'E')

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_received_wsu_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_choice_form_send(primary_key, 'W')
        self.blood_shipped_to_wsu(primary_key)
        response = self.blood_received_at_wsu(primary_key)

        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/blood/")


    #View has form tests

    def test_echo_2_bio_entry_whole_blood_shows_initial_form_for_collected(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        logging.debug(response.context)
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioForm)

    def test_echo_2_bio_entry_whole_blood_shows_incentive_form_after_collected(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        self.blood_collected_form_send(primary_key, 'plasma', False)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.critical(response.context)
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)


    def test_echo_2_bio_entry_whole_blood_shows_shipped_choice_form_after_incentive(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        self.blood_collected_form_send(primary_key, 'plasma', False)
        self.blood_incentive_form_send(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.critical(response.context)
        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_bio_page_shows_echo_shipped_form_if_collected_not_null_and_shipped_echo_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', False)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_choice_form_send(primary_key, 'E')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['shipped_echo_form'], ShippedtoEchoForm)

    def test_echo2_bio_page_shows_wsu_shipped_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', False)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_choice_form_send(primary_key, 'W')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUForm)

    def test_echo2_bio_page_shows_received_at_wsu_form_if_shipped_at_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', False)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_choice_form_send(primary_key, 'W')
        self.blood_shipped_to_wsu(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['received_wsu_form'], ReceivedatWSUForm)

    #View updates data tests

    def test_echo2_bio_entry_blood_updates_serum_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        self.blood_collected_form_send(primary_key, 'serum', True)
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
        self.blood_collected_form_send(primary_key, 'plasma', True)
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
        self.blood_collected_form_send(primary_key, 'whole_blood', True)
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
        self.blood_collected_form_send(primary_key, 'buffy_coat', True)
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
        self.blood_collected_form_send(primary_key, 'red_blood_cells', True)
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
        self.blood_collected_form_send(primary_key, 'red_blood_cells', False)
        with self.assertRaises(CaregiverBiospecimen.DoesNotExist):
            primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')


    def test_echo2_bio_entry_blood_does_not_update_plasma_if_checkbox_not_checked(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        self.blood_collected_form_send(primary_key, 'plasma', False)
        primary_key = self.create_bio_specimen(caregiver_id='P7000',collection_type='Plasma')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key)

        self.assertNotEqual(whole_blood.status_fk.collected_fk.collected_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.stored_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.processed_date_time,
                         datetime.datetime(2023, 5, 5, 9, 5, 5, tzinfo=datetime.timezone.utc))
        self.assertNotEqual(whole_blood.status_fk.collected_fk.number_of_tubes,5)



    def test_echo_2_bio_entry_whole_blood_updates_shipped_to_wsu_data_for_associated_bloods(self):
        primary_key_whole_blood = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)
        logging.debug(f"whole blood status test: {whole_blood.status_fk}")
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key_whole_blood)
        self.blood_collected_form_send(primary_key_whole_blood, 'red_blood_cells', True)

        logging.debug(f"whole blood status test:  {whole_blood.status_fk}")
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo':['W']})

        response =  self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')
        red_blood_count = CaregiverBiospecimen.objects.get(pk=primary_key)
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        logging.debug(f" red blood count {red_blood_count.status_fk} whole blood {whole_blood.status_fk}")

        self.assertEqual(red_blood_count.status_fk.shipped_wsu_fk.shipped_date_time,whole_blood.status_fk.shipped_wsu_fk.shipped_date_time)

    def test_echo_2_bio_entry_whole_blood_updates_received_wsu_data_for_associated_bloods(self):
        primary_key_whole_blood = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)
        logging.debug(f"whole blood status test: {whole_blood.status_fk}")
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key_whole_blood)
        self.blood_collected_form_send(primary_key_whole_blood, 'red_blood_cells', True)

        logging.debug(f"whole blood status test:  {whole_blood.status_fk}")
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo':['W']})

        response =  self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        response =  self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')
        red_blood_count = CaregiverBiospecimen.objects.get(pk=primary_key)
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        logging.debug(f" red blood count {red_blood_count.status_fk} whole blood {whole_blood.status_fk}")

        self.assertEqual(red_blood_count.status_fk.received_wsu_fk.received_date_time,whole_blood.status_fk.received_wsu_fk.received_date_time)


    def test_echo_2_bio_entry_whole_blood_updates_shipped_to_echo_data_for_associated_bloods(self):
        primary_key_whole_blood = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key_whole_blood)
        self.blood_collected_form_send(primary_key_whole_blood, 'red_blood_cells', True)

        logging.debug(f"whole blood status test:  {whole_blood.status_fk}")
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo': ['E']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_echo/post/',
                                    data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5,
                                                                                                         5, 5)})

        primary_key = self.return_caregiver_bio_pk('P7000', 'Red Blood Cells', 'F')
        red_blood_count = CaregiverBiospecimen.objects.get(pk=primary_key)
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        logging.debug(f" red blood count {red_blood_count.status_fk} whole blood {whole_blood.status_fk}")

        self.assertEqual(red_blood_count.status_fk.shipped_echo_fk.shipped_date_time,
                         whole_blood.status_fk.shipped_echo_fk.shipped_date_time)

    def test_echo_2_bio_entry_whole_blood_does_not_update_shipped_to_echo_data_for_bloods_not_checked(self):
        primary_key_whole_blood = self.return_caregiver_bio_pk('P7000', 'Whole Blood', 'F')
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key_whole_blood)
        self.blood_collected_form_send(primary_key_whole_blood, 'red_blood_cells', True)

        logging.debug(f"whole blood status test:  {whole_blood.status_fk}")
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_choice/post/',
                                    data={'shipped_choice_form-shipped_to_wsu_or_echo': ['E']})

        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key_whole_blood}/shipped_echo/post/',
                                    data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5,
                                                                                                         5, 5)})
        self.create_bio_specimen(caregiver_id='P7000',collection_type='Plasma')
        primary_key = self.return_caregiver_bio_pk('P7000', 'Plasma',trimester=None)
        self.add_collected_fk_to_biospecimen(biospecimen_pk=primary_key)
        self.add_shipped_echo_to_biospecimen(biospecimen_pk=primary_key)
        plasma = CaregiverBiospecimen.objects.get(pk=primary_key)
        whole_blood = CaregiverBiospecimen.objects.get(pk=primary_key_whole_blood)

        logging.debug(f" red blood count {plasma.status_fk} whole blood {whole_blood.status_fk}")


        self.assertNotEqual(plasma.status_fk.shipped_echo_fk.shipped_date_time,
                         whole_blood.status_fk.shipped_echo_fk.shipped_date_time)




class ChildBiospecimenPage(DatabaseSetup):

    def send_kit(self,primary_key,kit_sent):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={"initial_bio_form-collected_not_collected_kit_sent": f'{kit_sent}',
                                          "initial_bio_form_button": ['Submit']
                                          })
        return response

    def send_kit_form(self,primary_key,bio_id):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={"kit_sent_form-kit_sent_date": '2023-09-03',
                                          'kit_sent_form-echo_biospecimen_id': bio_id,
                                          'kit_sent_form_button':['Submit']
                                          })
        return response

    def send_collected_form(self,primary_key,collection_type):
        if collection_type in ('Urine','Stool'):
            response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                        data={"collected_child_form-in_person_remote": 'I',
                                              "collected_child_form-date_received":'2023-09-03',
                                              "collected_child_form-number_of_tubes":'4',
                                              "collected_form_button": ['Submit']
                                              })
        elif collection_type==('Bloodspots'):
            response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                        data={"collected_child_form-in_person_remote": 'I',
                                              "collected_child_form-date_received":'2023-09-03',
                                              "collected_child_form-number_of_cards":'4',
                                              "collected_form_button": ['Submit']
                                              })
        elif collection_type==('Tooth'):
            response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                        data={"collected_child_form-date_collected":'2023-09-03',
                                              "collected_form_button": ['Submit']})
        return response

    def send_incentive_form(self,primary_key):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={'child_incentive_form-incentive_date': ['2023-09-03'],
                                          'incentive_form_button': ['Submit']})
        logging.debug(response.content)
        return response

    def send_wsu_or_echo(self,primary_key,e_or_w):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={'child_shipped_choice_form-shipped_to_wsu_or_echo': [f'{e_or_w}'],
                                          'shipped_choice_form_button': ['Submit']})
        return response

    def send_to_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={'child_shipped_to_wsu_form-shipped_date_and_time': ['2023-09-27 12:52:26'],
                                          'shipped_to_wsu_form_button': ['Submit']})
        return response

    def received_at_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                    data={'child_received_at_wsu_form-received_date_time': ['2023-09-27 12:52:26'],
                                          'shipped_to_wsu_form_button': ['Submit']})
        return response

    def return_child_bio_pk(self,child_id,collection_type,age):
        child_object = Child.objects.get(charm_project_identifier=child_id)
        child_biospecimen = ChildBiospecimen.objects.get(child_fk=child_object,
                                                         collection_fk__collection_type_fk__collection_type=collection_type,
                                                         age_category_fk__age_category=age)

        return child_biospecimen.pk

    def test_echo2_initial_child_returns_correct_template(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/child_biospecimen_initial.html')

    def test_echo2_initial_child_urine_shows_urine(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertContains(response,'Urine')

    def test_echo2_initial_child_urine_shows_correct_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormPostNatal)

    def test_echo2_initial_child_tooth_shows_correct_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Tooth', 'ST')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormChildTooth)

    def test_echo2_initial_child_urine_redirects_after_post_kit_sent(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_post_not_collected(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'N')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_no_declined(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'X')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_declined_if_declined(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'X')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertContains(response,'Declined')

    def test_echo2_initial_child_urine_shows_declined_form_if_declined(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'X')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['declined_form'], DeclinedForm)

    def test_echo2_initial_child_urine_shows_kit_sent_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'K')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_initial_child_tooth_shows_kit_sent_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Tooth', 'ST')
        response = self.send_kit(primary_key,'K')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_initial_child_urine_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildUrineStoolForm)

    def test_echo2_initial_kit_sent_form_assigns_bio_id_child_bio(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        child_bio = ChildBiospecimen.objects.get(pk=primary_key)
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        child_bio = ChildBiospecimen.objects.get(pk=primary_key)
        self.assertEqual(child_bio.biospecimen_id,'5555555')

    def test_echo2_initial_child_bloodspots_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'ZF')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildBloodSpotForm)

    def test_echo2_initial_child_tooth_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Tooth', 'ST')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildToothForm)


    def test_echo2_initial_child_bloodspots_12_to_13_shows_collected_form(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'TT')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['collected_child_form'], CollectedChildBloodSpotHairFormOneYear)

    def test_echo2_initial_child_bloodspots_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'ZF')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_bloodspots_12_to_13_redirects_after_kit_sent_form_submitted(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'TT')
        response = self.send_kit(primary_key,'K')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_bloodspots_redirects_after_collected_form_submitted(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Bloodspots')
        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_collected_form_submitted(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_wsu_or_echo_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_initial_child_urine_shows_incentive_form_after_collection_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_initial_child_bloodspot_3_months_shows_wsu_or_echo_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Bloodspots')
        response = self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        logging.debug(response.content.decode())

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_initial_child_stool_3_months_shows_wsu_or_echo_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Stool', 'ZF')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        self.send_collected_form(primary_key,'Stool')
        response = self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceForm)

    def test_echo2_initial_child_bloodspots_12_months_shows_echo_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'TT')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        self.send_collected_form(primary_key,'Bloodspots')
        response = self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertNotContains(response,'Shipped to WSU')

    def test_echo2_initial_child_bloodspot_12_months_shows_echo_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Bloodspots', 'TT')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        self.send_collected_form(primary_key,'Stool')
        self.send_incentive_form(primary_key)

        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceEchoForm)

    def test_echo2_initial_child_tooth_6_year_shows_echo_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Tooth', 'ST')
        self.send_kit(primary_key,'K')
        self.send_kit_form(primary_key,bio_id='5555555')
        self.send_collected_form(primary_key,'Tooth')
        self.send_incentive_form(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')

        self.assertIsInstance(response.context['shipped_choice_form'], ShippedChoiceEchoForm)

    def test_echo2_initial_child_urine_redirects_after_shipped_choice_form_echo(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'E')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_shipped_to_echo_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key, 'E')

        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')


        self.assertIsInstance(response.context['shipped_to_echo_form'], ShippedtoEchoForm)

    def test_echo2_initial_child_urine_redirects_after_shipped_echo_form(self):
            primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
            self.send_kit(primary_key, 'K')
            response = self.send_kit_form(primary_key,bio_id='5555555')
            response = self.send_collected_form(primary_key,'Urine')
            response = self.send_incentive_form(primary_key)
            response = self.send_wsu_or_echo(primary_key,'E')

            response = self.client.post(f'/biospecimen/child/7002M1/{primary_key}/initial/',
                                        data={'child_shipped_to_echo_form-shipped_date_and_time': '2023-09-27 12:52:26',
                                              'shipped_to_echo_form_button':['Submit']})

            self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_redirects_after_shipped_choice_form_wsu(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'W')

        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_shipped_to_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key, 'W')
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        self.assertIsInstance(response.context['shipped_to_wsu_form'], ShippedtoWSUFormChild)
        
    def test_echo2_initial_child_urine_redirects_after_shipped_to_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'W')
        response = self.send_to_wsu(primary_key)
        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

    def test_echo2_initial_child_urine_shows_received_at_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key,'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key, 'W')
        response = self.send_to_wsu(primary_key)
        response = self.client.get(f'/biospecimen/child/7002M1/{primary_key}/initial/')
        logging.debug(f"response {response.content.decode()}")
        self.assertIsInstance(response.context['received_at_wsu_form'], ReceivedatWSUForm)

    def test_echo2_initial_child_urine_redirects_after_received_at_wsu_form_after_submission(self):
        primary_key = self.return_child_bio_pk('7002M1', 'Urine', 'ZF')
        self.send_kit(primary_key, 'K')
        response = self.send_kit_form(primary_key,bio_id='5555555')
        response = self.send_collected_form(primary_key,'Urine')
        response = self.send_incentive_form(primary_key)
        response = self.send_wsu_or_echo(primary_key,'W')
        response = self.send_to_wsu(primary_key)
        response = self.received_at_wsu(primary_key)
        self.assertRedirects(response, f'/biospecimen/child/7002M1/{primary_key}/initial/')

class CheckthatLoginRequiredforBiospecimen(DatabaseSetup):

    def setUp(self):
        self.client.logout()

    def test_that_login_required_for_biospecimen_history_page(self):
        response = self.client.get(f'/biospecimen/history/')
        self.assertTemplateNotUsed(response, 'biospecimen/biospecimen_history.html')

    def test_that_login_required_for_biospecimen_entry_page(self):
        response = self.client.get(f'/biospecimen/entry/')
        self.assertTemplateNotUsed(response, 'biospecimen/biospecimen_entry.html')

    def test_that_login_required_for_biospecimen_child_page(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertTemplateNotUsed(response, 'biospecimen/child_biospecimen.html')

    def test_that_login_required_for_caregiver_biospecimen_history_page(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/1/history/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_history.html')

    def test_that_login_required_for_biospecimen_initial_page(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_that_login_required_for_biospecimen_blood_page(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_that_login_required_for_biospecimen_child_entry_page(self):
        response = self.client.get(f'/biospecimen/child/7000M1/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')
