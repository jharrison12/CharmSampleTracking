import logging
import unittest
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen,\
    ShippedECHO, Collected, Caregiver, Project, Child,User,Component,PregnancyTrimester
import datetime
from django.utils import timezone
from biospecimen.forms import IncentiveForm, ProcessedBiospecimenForm, StoredBiospecimenForm, \
    ShippedBiospecimenForm, ReceivedBiospecimenForm, CollectedBiospecimenUrineForm, InitialBioForm, ShippedChoiceForm, \
    ShippedtoWSUForm, ShippedtoEchoForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm, \
    ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,InitialBioFormChildTooth,\
    CollectedChildToothForm,DeclinedForm,ReceivedatWSUForm,ShippedtoMSUForm,CollectedBiospecimenHairSalivaForm,ShippedtoWSUFormBlood,ReceivedatWSUBloodForm
from biospecimen.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)


class CaregiverEcho2BiospecimenPageUrine(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester,age_category=None, project='ECHO2'):
        logging.debug(f"chrarm_id {charm_id} collection_type {collection_type} trimester {trimester} age_category {age_category} project {project}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)

        return caregiverbio.pk

    def collected_send_form(self, primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/',
                                    data={"urine_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "urine_form-processed_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "urine_form-stored_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "urine_form-number_of_tubes": 5})
        return response


    def initial_send_form(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected": c_n_or_x,
                                          })
        return response

    def kit_sent_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/kit_sent/post/',
                         data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                               'kit_sent_form-echo_biospecimen_id': 3333})

        return response

    def incentive_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })
        return response

    def shipped_choice_send_form(self,primary_key,w_or_e):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_choice/post/',
                                    data={"shipped_choice_form-shipped_to_wsu_or_echo": w_or_e,
                                          })
        return response

    def shipped_to_echo_echo_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_echo/post/',
                         data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})

        return response


    def shipped_to_wsu_send_form(self,primary_key):
        response =  self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def received_at_wsu_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    #TEMPLATES

    def test_echo2_initial_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_bio_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    def test_echo2_bio_page_shows_caregiver_id(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response, '4100')

    def test_echo2_bio_page_shows_trimester_if_urine(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response, 'Trimester: Second')

    def test_echo2_bio_page_does_not_show_formalin_if_urine(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertNotContains(response, 'formalin')

    def test_echo2_bio_entry_urine_shows_user_who_is_logged_in_after_submitted(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key, 'C')
        response = self.collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response,'Logged By: testuser')

    def test_echo2_bio_page_shows_shipped_to_wsu_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key, 'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key, 'W')
        response = self.shipped_to_wsu_send_form(primary_key)
        response = self.received_at_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response, 'Courier: FedEx')

    def test_echo2_bio_page_shows_shipped_by_user(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key, 'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key, 'W')
        response = self.shipped_to_wsu_send_form(primary_key)
        response = self.received_at_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response, 'Shipped By: testuser')

    def test_echo2_bio_page_shows_shipped_to_echo_data_if_complete(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_wsu_send_form(primary_key)
        response = self.received_at_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertContains(response, 'Shipped Date Time:')

    #REDIRECTS

    def test_echo2_bio_entry_urine_collected_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key, 'C')
        response = self.collected_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_urine_initial_posts_to_initial_post_view(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_urine_initial_posts_to_initial_post_view_not_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'N')
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_urine_initial_posts_to_initial_post_view_denied(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'X')
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_urine_incentive_form_redirects_to_entry(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_entry_shipped_choice_redirects_after_post_wsu(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key,'W')
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_entry_urine_shipped_choice_redirects_after_post_echo(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key,'E')
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_urine_entry_shipped_echo_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key,'E')
        response = self.shipped_to_echo_echo_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_urine_entry_received_urine_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_choice_send_form(primary_key,'W')
        response = self.shipped_to_wsu_send_form(primary_key)
        response = self.received_at_wsu_send_form(primary_key)
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    #FORMS
        #Urine

    def test_echo2_bio_page_shows_initial_collected_or_not_form_if_no_collected_object_and_collection_urine(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioForm)

    def test_echo2_bio_page_does_not_show_collected_urine_form_if_no_collected_object_and_collection_urine(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertNotIsInstance(response.context['collected_form'], CollectedBiospecimenUrineForm)

    def test_echo2_bio_entry_shows_incentive_form_if_collected_form_sent(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        response = self.initial_send_form(primary_key,'C')
        response = self.collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_bio_page_shows_wsu_shipped_form_if_incentive_submitted(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUForm)

    def test_echo2_bio_page_shows_wsu_received_form_if_shipped_to_wsu_form_sent(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        self.initial_send_form(primary_key, 'C')
        self.collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        # self.shipped_choice_send_form(primary_key, 'W')
        self.shipped_to_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        logging.debug(f"{response.content.decode()}")
        self.assertIsInstance(response.context['received_at_wsu_form'], ReceivedatWSUForm)

    def test_echo2_bio_page_shows_shipped_echo_form_if_received_at_wsu(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'U', 'S')
        self.initial_send_form(primary_key,'C')
        self.collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        self.shipped_to_wsu_send_form(primary_key)
        self.received_at_wsu_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_echo_form'], ShippedtoEchoForm)

class CaregiverEcho2BiospecimenPageHairSaliva(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester,age_category=None, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)
        return caregiverbio.pk

    def collected_send_form(self, primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/',
                                    data={"id_urine_form-collected_date_time": timezone.datetime(2023, 5, 5, 5, 5, 5),
                                          "id_urine_form-processed_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "id_urine_form-stored_date_time": timezone.datetime(2023, 5, 5, 5, 5,5),
                                          "id_urine_form-number_of_tubes": 5})
        return response

    def hair_saliva_collected_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/',
                         data={'hair_saliva_form-in_person_remote': 'I',
                               'hair_saliva_form-date_collected': '2023-09-27',
                               'hair_saliva_form-incentive_date': '2023-09-27'})

        return response

    def initial_send_form_hair_saliva(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected_kit_sent": c_n_or_x,
                                          })
        return response

    def kit_sent_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/kit_sent/post/',
                         data={'kit_sent_form-kit_sent_date': ['2023-09-30'],
                               'kit_sent_form-echo_biospecimen_id': 3333})

        return response

    def incentive_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })
        return response

    def shipped_to_msu_form(self, primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_msu/post/',
                                    data={"shipped_to_msu_form-date_time_shipped": timezone.datetime(2023,4, 5, 5, 5, 5),
                                          })
        return response

    def received_at_msu_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_msu/post/',
                                    data={
                                        "received_at_msu_form-received_time_shipped": timezone.datetime(2023, 4, 5, 5, 5, 5),
                                        })
        return response

    def shipped_to_echo_send_form(self, primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_echo/post/',
                         data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})

        return response


    def shipped_to_wsu_send_form(self,primary_key):
        response =  self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def received_at_wsu_send_form(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    #TEMPLATES

    def test_echo2_bio_page_hair_uses_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None, age_category='ZF')
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/')

        self.assertTemplateUsed(response, "biospecimen/caregiver_biospecimen_initial.html")

    def test_echo2_entry_bio_hair_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None, age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    def test_echo2_bio_page_saliva_uses_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None, age_category='ZF')
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/')

        self.assertTemplateUsed(response, "biospecimen/caregiver_biospecimen_initial.html")

    def test_echo2_entry_bio_saliva_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None, age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry.html')

    #REDIRECTS

    def test_echo2_bio_page_hair_redirects_after_initial_kit_sent_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_hair_redirects_after_initial_declined_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'X')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_hair_redirects_after_initial_not_collected_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'N')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_hair_redirects_after_kit_sent_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_hair_redirects_after_collected_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_hair_redirects_after_incentive_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_hair_redirects_after_shipped_to_msu_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_hair_redirects_after_received_msu_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        response = self.received_at_msu_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_hair_redirects_after_shipped_echo_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        response = self.received_at_msu_send_form(primary_key)
        response = self.shipped_to_echo_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    #REDIRECTS
        #SALIV
    
    def test_echo2_bio_page_saliva_redirects_after_initial_kit_sent_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_saliva_redirects_after_initial_declined_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'X')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_saliva_redirects_after_initial_not_collected_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'N')
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/")

    def test_echo2_bio_page_saliva_redirects_after_kit_sent_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_collected_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_incentive_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_shipped_to_msu_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_received_msu_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        response = self.received_at_msu_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_shipped_echo_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        response = self.received_at_msu_send_form(primary_key)
        response = self.shipped_to_echo_send_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    def test_echo2_bio_page_saliva_redirects_after_received_wsu_form_submission(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'L', trimester=None,age_category='ZF')
        response = self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.kit_sent_send_form(primary_key)
        response = self.hair_saliva_collected_send_form(primary_key)
        response = self.incentive_send_form(primary_key)
        response = self.shipped_to_msu_form(primary_key)
        self.assertRedirects(response,f"/biospecimen/caregiver/4100/{primary_key}/entry/")

    #FORMS
        #HAIR

    def test_echo2_bio_page_initial_form_shows_denied_not_collected_kit_sent_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/initial/')
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioFormPostNatal)

    def test_echo2_bio_page_shows_kit_sent_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        self.initial_send_form_hair_saliva(primary_key,'K')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/hairandsaliva/')
        self.assertIsInstance(response.context['kit_sent_form'], KitSentForm)

    def test_echo2_bio_page_shows_collected_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        self.initial_send_form_hair_saliva(primary_key,'K')
        self.kit_sent_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['collected_form'], CollectedBiospecimenHairSalivaForm)

    def test_echo2_bio_page_shows_incentive_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        self.initial_send_form_hair_saliva(primary_key,'K')
        self.kit_sent_send_form(primary_key)
        self.hair_saliva_collected_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_bio_page_shows_shipped_echo_form_if_hair_or_salvia(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'H', trimester=None,age_category='ZF')
        self.initial_send_form_hair_saliva(primary_key,'K')
        self.kit_sent_send_form(primary_key)
        self.hair_saliva_collected_send_form(primary_key)
        self.incentive_send_form(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/')
        self.assertIsInstance(response.context['shipped_to_msu_form'], ShippedtoMSUForm)

class CaregiverEcho2BiospecimenPageBlood(DatabaseSetup):
    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

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

    def blood_initial_send_form(self, primary_key,c_n_or_x):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/initial/post/',
                                    data={"initial_form-collected_not_collected": c_n_or_x,
                                          })
        return response

    def blood_incentive_form_send(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/incentive/post/',
                                    data={"incentive_form-incentive_date": '2023-09-03',
                                          })

        return response

    def blood_shipped_to_wsu(self,primary_key, false_or_true,type_of_blood):
        response =  self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          f'shipped_to_wsu_form-{type_of_blood}': false_or_true,
                                          f'shipped_to_wsu_form-{type_of_blood}_number_of_tubes': 5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def blood_received_at_wsu(self,primary_key,type_of_blood,false_or_true):
        if false_or_true:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                        data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                              f'received_at_wsu_form-{type_of_blood}':type_of_blood,
                                              f'received_at_wsu_form-{type_of_blood}_number_of_tubes': 5})
        else:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                        data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    def shipped_to_echo_send_form(self,primary_key,type_of_blood, false_or_true):
        if false_or_true:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_echo/post/',
                         data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5),
                               f'shipped_to_echo_form-{type_of_blood}':type_of_blood,
                               f'shipped_to_echo_form-{type_of_blood}_number_of_tubes':5})
        else:
            response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_echo/post/',
                         data={'shipped_to_echo_form-shipped_date_and_time': timezone.datetime(2023, 5, 5, 5, 5, 5)})


        return response


    #Template Tests

    def test_echo2_initial_bio_blood_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/initial/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_echo2_entry_bio_blood_page_returns_correct_template(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        self.assertTemplateUsed(response, 'biospecimen/caregiver_biospecimen_entry_blood.html')
    #move


    def test_echo2_bio_page_shows_trimester_if_blood(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        self.assertContains(response, 'Trimester: Second')

    def test_echo2_bio_page_shows_collected_blood_form_if_blood_and_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        self.assertContains(response, '<input type="checkbox" name="blood_form-serum')
        self.assertContains(response, '<input type="checkbox" name="blood_form-whole_blood')
        self.assertContains(response, '<input type="checkbox" name="blood_form-plasma')
        self.assertContains(response, '<input type="checkbox" name="blood_form-buffy_coat')
        self.assertContains(response, '<input type="checkbox" name="blood_form-red_blood_cells')

    def test_echo2_bio_entry_blood_shows_updated_values_if_posted(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'plasma',false_or_true=True)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertContains(response,'Plasma Number of Tubes: 5')

    def test_echo2_bio_entry_plasma_blood_is_checked_and_not_editable(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'plasma',false_or_true=True)
        self.blood_incentive_form_send(primary_key)
        response = self.blood_shipped_to_wsu(primary_key,type_of_blood='plasma',false_or_true=True)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertContains(response, '<input class="form-check-input" type="checkbox" value="" id="flexCheckCheckedDisabled" checked disabled>')

    def test_blood_collected_creates_row_in_component_that_links_to_blood_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,
                                               caregiver_biospecimen_fk__trimester_fk__trimester='S',
                                               component_type=Component.ComponentType.SERUM)
        logging.debug(component_test)
        self.assertEqual(component_test.collected_fk, caregiver_bio.status_fk.collected_fk)

    def test_blood_collected_creates_row_in_component_that_links_to_blood_shipped_wsu(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,
                                               caregiver_biospecimen_fk__trimester_fk__trimester='S',
                                               component_type=Component.ComponentType.SERUM)
        logging.debug(component_test)
        self.assertEqual(component_test.shipped_wsu_fk, caregiver_bio.status_fk.shipped_wsu_fk)

    def test_blood_collected_creates_row_in_component_that_links_to_blood_received_at_wsu(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        self.blood_received_at_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,
                                               caregiver_biospecimen_fk__trimester_fk__trimester='S',
                                               component_type=Component.ComponentType.SERUM)
        logging.debug(component_test)
        self.assertEqual(component_test.received_wsu_fk, caregiver_bio.status_fk.received_wsu_fk)

    def test_blood_collected_creates_row_in_component_that_links_to_blood_shipped_to_echo(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        self.blood_received_at_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        self.shipped_to_echo_send_form(primary_key,type_of_blood='serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,
                                               caregiver_biospecimen_fk__trimester_fk__trimester='S',
                                               component_type=Component.ComponentType.SERUM)
        logging.debug(component_test)
        self.assertEqual(component_test.shipped_echo_fk, caregiver_bio.status_fk.shipped_echo_fk)

    # Redirection tests

    def test_echo2_bio_blood_form_redirects_after_post(self):
        #not sure what this is testing
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        response = self.blood_initial_send_form(primary_key, 'C')
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/',
                                    data={"id_blood_form-serum": True,
                                          })

        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")


    def test_echo2_bio_blood_initial_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        response = self.blood_initial_send_form(primary_key,'C')

        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_collected_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key,'C')
        response = self.blood_collected_form_send(primary_key,"serum",True)

        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_incentive_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key,'C')
        self.blood_collected_form_send(primary_key,"serum",True)
        response = self.blood_incentive_form_send(primary_key)

        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")

    def test_echo2_bio_blood_shipped_wsu_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        response = self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)

        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")


    def test_echo2_bio_blood_received_wsu_form_redirects_after_post(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, "serum", True)
        self.blood_incentive_form_send(primary_key)
        self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        response = self.blood_received_at_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        self.assertRedirects(response, f"/biospecimen/caregiver/4100/{primary_key}/entry/blood/")

    #View has form tests

    def test_echo_2_bio_entry_whole_blood_shows_initial_form_for_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/initial/')
        logging.debug(response.context)
        self.assertIsInstance(response.context['initial_bio_form'], InitialBioForm)

    def test_echo_2_bio_entry_whole_blood_shows_incentive_form_after_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'plasma',5)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        logging.debug(response.context)
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_echo2_bio_page_shows_wsu_shipped_form_if_collected_not_null_and_shipped_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', False)
        self.blood_incentive_form_send(primary_key)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['shipped_wsu_form'], ShippedtoWSUFormBlood)

    def test_echo2_bio_page_shows_received_at_wsu_form_if_shipped_at_wsu_not_null(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        caregiver_bio = CaregiverBiospecimen.objects.get(pk=primary_key)
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'plasma',5)
        self.blood_incentive_form_send(primary_key)
        response = self.blood_shipped_to_wsu(primary_key,type_of_blood='serum',false_or_true=True)
        response = self.client.get(f'/biospecimen/caregiver/4100/{primary_key}/entry/blood/')
        logging.debug(response.content.decode())
        self.assertIsInstance(response.context['received_wsu_form'], ReceivedatWSUBloodForm)

    #View updates data tests

    def test_echo2_bio_entry_blood_updates_serum_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'serum', True)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        serum_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='S')
        self.assertEqual(serum_component.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_plasma_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', True)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        plasma_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='P')
        self.assertEqual(plasma_component.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_whole_blood_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'whole_blood', True)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        whole_blood_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='W')
        self.assertEqual(whole_blood_component.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_buffy_coat_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'buffy_coat', True)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        buffy_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='F')
        self.assertEqual(buffy_component.number_of_tubes,5)

    def test_echo2_bio_entry_blood_updates_red_blood_count_if_checkbox_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'red_blood_cells', True)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        rbc_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='R')
        self.assertEqual(rbc_component.number_of_tubes,5)

    def test_echo2_bio_entry_blood_does_not_update_plasma_if_checkbox_not_checked(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key, 'plasma', False)
        blood = CaregiverBiospecimen.objects.get(pk=primary_key)
        plasma_component = Component.objects.get(caregiver_biospecimen_fk=blood,component_type='P')
        self.assertNotEqual(plasma_component.number_of_tubes,5)


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
        response = self.client.get(f'/biospecimen/child/4100F1/')
        self.assertTemplateNotUsed(response, 'biospecimen/child_biospecimen.html')

    def test_that_login_required_for_caregiver_biospecimen_history_page(self):
        response = self.client.get(f'/biospecimen/caregiver/4100/1/history/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_history.html')

    def test_that_login_required_for_biospecimen_initial_page(self):
        response = self.client.get(f'/biospecimen/caregiver/4100/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_that_login_required_for_biospecimen_blood_page(self):
        response = self.client.get(f'/biospecimen/caregiver/4100/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')

    def test_that_login_required_for_biospecimen_child_entry_page(self):
        response = self.client.get(f'/biospecimen/child/4100/1/initial/')
        self.assertTemplateNotUsed(response, 'biospecimen/caregiver_biospecimen_initial.html')