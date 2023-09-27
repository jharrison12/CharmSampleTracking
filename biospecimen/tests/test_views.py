import logging
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
from biospecimen.models import Collection, Status,ChildBiospecimen,CaregiverBiospecimen,Processed
import datetime
from django.utils import timezone
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm,ProcessedBiospecimenForm
from django.utils.html import escape
from dataview.tests.db_setup import DatabaseSetup

@unittest.skip
class CaregiverBiospecimenPageTest(DatabaseSetup):

    def get_biospecimen_page(self,biospecimen_id):
        response = self.client.get(f'/biospecimen/caregiver/{biospecimen_id}/')
        return response

    def test_caregiver_biospecimen_page_returns_correct_template(self):
        self.assertTemplateUsed(self.get_biospecimen_page('P7000'),'biospecimen/caregiver_biospecimen.html')

    def test_caregiver_biospecimen_page_contains_urine_1(self):
        self.assertContains(self.get_biospecimen_page('P7000'),'Serum 1: Completed')

    def test_caregiver_b_biospecimen_does_not_appear_in_caregiver_a_page(self):
        self.assertNotContains(self.get_biospecimen_page('P7001'),'Serum 1: Completed')

    def test_caregiver_a_bio_page_shows_all_urines(self):
        self.assertContains(self.get_biospecimen_page('P7000'),"Urine 1")
        self.assertContains(self.get_biospecimen_page('P7000'),"Urine EC")

    def test_caregiver_a_bio_page_shows_hair(self):
        self.assertContains(self.get_biospecimen_page('P7000'),"Prenatal Hair: Completed")

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

    def get_biospecimen_entry_page(self,biospecimen_id):
        response = self.client.get(f'/biospecimen/caregiver/{biospecimen_id}/entry/')
        return response

    def test_using_correct_template(self):
        self.assertTemplateUsed(self.get_biospecimen_entry_page('P7000'), 'biospecimen/caregiver_biospecimen_entry.html')

    def test_caregiver_bio_entry_page_uses_bio_form(self):
        self.assertIsInstance(self.get_biospecimen_entry_page('P7000').context['bio_form'], CaregiverBiospecimenForm)

    def test_bio_entry_redirects_after_post(self):

        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/', data={'bio_form-collection_fk':self.placenta_two.pk,
                                                                                       'bio_form-status_fk':self.collected.pk,
                                                                                       'bio_form-biospecimen_date':datetime.date(2023,8,23),
                                                                                       #'incentive_fk':  self.incentive_one.pk,
                                                                                       'bio_form-caregiver_fk': self.first_caregiver.pk,
                                                                                       'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                                                                       'incentive_form-incentive_date':datetime.date(2023,8,23),
                                                                                       'incentive_form-incentive_amount':1,
                                                                                       })

        self.assertRedirects(response,f"/biospecimen/caregiver/P7000/")

    def test_unique_validation_errors_are_sent_back_to_entry_page(self):
        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/', data={'bio_form-collection_fk':self.placenta.pk,
                                                                                       'bio_form-status_fk':self.collected.pk,
                                                                                       'bio_form-biospecimen_date':datetime.date(2023,8,23),
                                                                                       'bio_form-caregiver_fk': self.first_caregiver.pk,
                                                                                       'incentive_fk':  self.incentive_one.pk,
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

        response = self.client.post(f'/biospecimen/caregiver/P7000/entry/', data={'bio_form-collection_fk':self.placenta_two.pk,
                                                                                       'bio_form-status_fk':self.collected.pk,
                                                                                       'bio_form-biospecimen_date':datetime.date(2023,8,23),
                                                                                       #'incentive_fk':  self.incentive_one.pk,
                                                                                       'bio_form-caregiver_fk': self.first_caregiver.pk,
                                                                                       'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                                                                       'incentive_form-incentive_date':datetime.date(2023,8,23),
                                                                                       'incentive_form-incentive_amount':1,
                                                                                       })

        placenta_two = CaregiverBiospecimen.objects.filter(collection_fk__collection_type="Placenta").filter(collection_fk__collection_number=2).first()

        correct_incentive = Incentive.objects.filter(incentive_amount=1).first()

        self.assertEqual(placenta_two.incentive_fk,correct_incentive)


class ChildBiospecimenPage(DatabaseSetup):

    def test_child_biospecimen_page_uses_correct_template(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertTemplateUsed(response,'biospecimen/child_biospecimen.html')

    def test_child_biospecimen_page_has_header(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertContains(response,'Child ID: 7000M1')

    @unittest.skip
    def test_child_biospecimen_page_has_urine(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        self.assertContains(response,'Urine 6: Completed')

    def test_child_biospecimen_contains_all_child_biospecimens(self):
        response = self.client.get(f'/biospecimen/child/7000M1/')
        child_bios = ChildBiospecimen.objects.values('collection_fk__collection_type')
        child_bios_list = list(set(value for dic in child_bios for value in dic.values()))
        for value in child_bios_list:
            self.assertContains(response, value)

class CaregiverSingleBiospecimenPage(DatabaseSetup):

    def test_caregiver_blood_spot_page_uses_correct_template(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/blood_spots/')
        self.assertTemplateUsed(response,'biospecimen/caregiver_biospecimen_blood_spots.html')

    def test_caregiver_blood_spot_contains_blood_spot_id(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/blood_spots/')
        self.assertContains(response,'ID: 1111BS')

    def test_caregiver_blood_spot_page_uses_processed_form_if_no_processed_data(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/blood_spots/')
        blood_spots = Collection.objects.get(collection_type='Bloodspots')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7001')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=blood_spots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.critical(f"processed is {processed_one.count()}")
        self.assertIsInstance(response.context['processed_form'], ProcessedBiospecimenForm)

    def test_caregiver_blood_spot_page_does_not_show_processed_form_if_processed_data(self):
        response = self.client.get(f'/biospecimen/caregiver/P7000/blood_spots/')
        blood_spots = Collection.objects.get(collection_type='Bloodspots')
        caregiver = Caregiver.objects.get(charm_project_identifier='P7000')
        processed_one = Processed.objects.filter(status__caregiverbiospecimen__collection_fk=blood_spots,
                                                 status__caregiverbiospecimen__caregiver_fk=caregiver)

        logging.critical(f"processed is {processed_one.count()}")
        self.assertNotContains(response,'<form>',html=True)

    def test_caregiver_blood_spot_page_redirects_after_post(self):

        response = self.client.post(f'/biospecimen/caregiver/P7000/blood_spots/',
                                    data={'processed_form-collected_date_time':datetime.datetime.now(),
                                          "processed_form-processed_date_time":datetime.datetime.now(),
                                          "processed_form-quantity":2,
                                          "processed_form-logged_date_time":datetime.datetime.now(),
                                          })

        self.assertRedirects(response,f"/biospecimen/caregiver/P7000/blood_spots/")

    def test_processed_form_links_to_status_caregiver(self):
        response = self.client.post(f'/biospecimen/caregiver/P7000/blood_spots/',
                                    data={'processed_form-collected_date_time':datetime.datetime.now(),
                                          "processed_form-processed_date_time":datetime.datetime.now(),
                                          "processed_form-quantity":5,
                                          "processed_form-logged_date_time":datetime.datetime.now(),
                                          "processed_form-outcome_fk":'C'
                                          })
        caregiver_object = CaregiverBiospecimen.objects.get(status_fk__processed_fk__quantity=5)
        self.assertEqual(caregiver_object.caregiver_fk.charm_project_identifier,'P7000')