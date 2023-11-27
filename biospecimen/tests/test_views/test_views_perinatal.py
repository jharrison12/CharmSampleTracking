import logging
import sqlite3
import unittest
from django.test import TestCase
from dataview.models import Caregiver, Project,Incentive,  Child,User
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen, Processed, Stored, \
    ShippedWSU, ShippedECHO, Collected
import datetime
from django.utils import timezone
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm, ShippedChoiceForm, \
    ShippedtoWSUForm, ShippedtoEchoForm,ReceivedatWSUForm,InitialBioFormPeriNatal,CollectedBiospecimenForm,CollectedBiospecimenPlacentaForm,\
ShippedtoWSUFormPlacenta
from django.utils.html import escape
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)

class CaregiverEcho2BiospecimenPagePlacenta(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester=None,age_category=None, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)
        return caregiverbio.pk

    def collected_send_form(self, primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/post/',
                                    data={"placenta_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "placenta_form-processed_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "placenta_form-placed_in_formalin": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          })
        return response


    def initial_send_form(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected_no_consent": c_n_or_x,
                                          })
        return response

    def kit_sent_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/kit_sent/post/',
                         data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                               'kit_sent_form-echo_biospecimen_id': 3333})

        return response

    def incentive_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })
        return response

    def shipped_choice_send_form(self,primary_key,w_or_e):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_choice/post/',
                                    data={"shipped_choice_form-shipped_to_wsu_or_echo": w_or_e,
                                          })
        return response

    def shipped_to_echo_echo_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_echo/post/',
                         data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})

        return response


    def shipped_to_wsu_send_form(self,primary_key):
        response =  self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def received_at_wsu_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/P7000/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    #TEMPLATES

    def test_echo2_initial_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    def test_echo2_bio_page_shows_caregiver_id(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'P7000')

    def test_echo2_bio_entry_Placenta_shows_user_who_is_logged_in_after_submitted(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response,'Logged By: testuser')

    def test_echo2_bio_page_shows_shipped_to_wsu_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        self.shipped_choice_send_form(primary_key,'W')
        self.shipped_to_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Courier: FedEx')

    def test_echo2_bio_page_shows_shipped_by_user(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key, 'C')
        self.collected_send_form(primary_key)
        self.shipped_choice_send_form(primary_key, 'W')
        self.shipped_to_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertContains(response, 'Shipped By: testuser')

    def test_echo2_bio_page_shows_shipped_to_echo_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        self.shipped_choice_send_form(primary_key,'W')
        self.shipped_to_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        # logging.debug(response.content.decode())
        # print html RESPONSE CONTENT DECODE
        self.assertContains(response, 'Shipped Date Time:')

    #REDIRECTS

    def test_echo2_bio_Placenta_initial_posts_to_initial_post_view(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_Placenta_initial_posts_to_initial_post_view_not_collected(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'N')
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_Placenta_initial_posts_to_initial_post_view_denied(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'O')
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_entry_Placenta_collected_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_Placenta_incentive_form_redirects_to_entry(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    def test_echo2_bio_entry_shipped_to_wsu_redirects_after_post_wsu(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_wsu_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")


    def test_echo2_bio_Placenta_entry_received_Placenta_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key,'W')
        response = self.received_at_wsu_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/P7000/{primary_key}/entry/")

    #FORMS
        #Placenta

    def test_echo2_bio_page_shows_initial_collected_or_not_form_if_no_collected_object_and_collection_Placenta(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormPeriNatal)

    def test_echo2_bio_page_does_not_show_collected_Placenta_form_if_no_collected_object_and_collection_Placenta(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertNotIsInstance(response.context['collected_form'], CollectedBiospecimenPlacentaForm)

    def test_echo2_bio_entry_shows_incentive_form_if_collected_form_sent(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_bio_page_shows_wsu_shipped_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUFormPlacenta)


    def test_echo2_bio_page_shows_wsu_received_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('P7000', 'Placenta')
        self.initial_send_form(primary_key, 'C')
        self.collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        self.shipped_choice_send_form(primary_key, 'W')
        self.shipped_to_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/P7000/{primary_key}/entry/')
        logging.debug(f"{response.context}")
        self.assertIsInstance(response.context['received_at_wsu_form'], ReceivedatWSUForm)

