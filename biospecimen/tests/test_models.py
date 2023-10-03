import logging
import sqlite3

from django.test import TestCase
from biospecimen.models import Collection,CaregiverBiospecimen,ChildBiospecimen,Status,Processed,Outcome,Stored,Shipped,\
    Received,Collected,Trimester,Perinatal
import datetime
from dataview.models import Caregiver,Incentive,Child
from dataview.tests.db_setup import DatabaseSetup
from django.utils import timezone
from django.core.exceptions import ValidationError

class BioSpecimenCaregiverModelsTest(DatabaseSetup):
    def test_biospecimen_links_to_mother_table(self):
        caregiver_bio_one = Caregiver.objects.filter(caregiverbiospecimen__collection_fk__collection_type_fk__collection_type='Urine')\
            .filter(charm_project_identifier='P7000').first()
        self.assertEqual(caregiver_bio_one,self.first_caregiver)

    def test_biospecimen_urine_links_to_two_caregivers(self):
        urine_samples = CaregiverBiospecimen.objects.filter(collection_fk__collection_type_fk__collection_type='Urine')\
            .filter(collection_fk__collection_number_fk__collection_number="F")
        self.assertEqual(urine_samples.count(),2)

    def test_biospecimen_links_to_incentive_table(self):
        first_incentive =  Incentive.objects.filter(caregiverbiospecimen__collection_fk__collection_type_fk__collection_type='Urine').first()
        self.assertEqual(first_incentive.incentive_amount,100)

    def test_caregiver_biospecimen_doesnt_allow_duplicates(self):
        caregiverbio_one = CaregiverBiospecimen(caregiver_fk=self.first_caregiver, collection_fk=self.serum_one,
                                                status_fk=self.status_outcome_processed_complete, biospecimen_date=datetime.date.today(),
                                                incentive_fk=self.incentive_one)
        with self.assertRaises(ValidationError):
            caregiverbio_one.full_clean()

    def test_caregiver_biospecimen_outcome_links_to_processed(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots')
        outcome = Outcome.objects.get(processed__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_stored(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots')
        stored = Stored.objects.create()
        outcome = Outcome.objects.get(stored__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_shipped(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots')

        outcome = Outcome.objects.get(shipped__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_received(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots')
        outcome = Outcome.objects.get(received__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_links_to_collected(self):
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',trimester_fk__trimester='F')
        caregiver = Caregiver.objects.get(caregiverbiospecimen__status_fk__collected_fk__number_of_tubes=5)
        self.assertEqual(caregiver,caregiver_bio.caregiver_fk)

    def test_caregiver_biospecimen_links_to_trimester(self):
        urine_tree = Collection.objects.get(collection_number_fk__collection_number='T',collection_type_fk__collection_type='Urine')
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk=urine_tree)
        trimester = Trimester.objects.get(trimester='F')
        self.assertEqual(caregiver.trimester_fk,trimester)

    def test_caregiver_biospecimen_outcome_links_to_perinatal(self):
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta',collection_number_fk=None)
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk=placenta)
        perinatal_event = Perinatal.objects.get(child_fk__charm_project_identifier='7000M1')
        self.assertEqual(caregiver.perinatal_fk,perinatal_event)


class ChildBiospecimenModelTest(DatabaseSetup):

    def test_child_links_to_biospecimen(self):
        urine = Collection.objects.get(collection_type_fk__collection_type='Urine',collection_number_fk__collection_number='T')
        test_child = Child.objects.filter(childbiospecimen__age_category_fk__age_category='EC',
                                          childbiospecimen__collection_fk=urine).first()
        self.assertEqual(test_child,self.child_one)

    def test_multiple_children_link_to_one_biospecimen(self):
        urine_collection = Collection.objects.get(collection_type_fk__collection_type='Urine',collection_number_fk__collection_number='T')
        urine = ChildBiospecimen.objects.filter(collection_fk=urine_collection)
        self.assertEqual(urine.count(),2)
