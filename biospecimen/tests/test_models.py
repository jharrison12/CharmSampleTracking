import logging
import sqlite3

from django.test import TestCase
from biospecimen.models import Collection,CaregiverBiospecimen,ChildBiospecimen,Status
import datetime
from dataview.models import Caregiver,Incentive,Child
from dataview.tests.test_models import ModelTest
from django.utils import timezone
from django.core.exceptions import ValidationError

class BioSpecimenCaregiverModelsTest(ModelTest):
    def test_biospecimen_links_to_mother_table(self):
        caregiver_bio_one = Caregiver.objects.filter(caregiverbiospecimen__collection_fk__collection_type='Urine')\
            .filter(charm_project_identifier='P7000').first()
        self.assertEqual(caregiver_bio_one,self.first_caregiver)

    def test_biospecimen_urine_links_to_two_caregivers(self):
        urine_samples = CaregiverBiospecimen.objects.filter(collection_fk__collection_type='Urine').filter(collection_fk__collection_number=1)
        self.assertEqual(urine_samples.count(),2)

    def test_biospecimen_links_to_incentive_table(self):
        first_incentive =  Incentive.objects.filter(caregiverbiospecimen__collection_fk__collection_type='Urine').first()
        self.assertEqual(first_incentive.incentive_amount,100)

    def test_caregiver_biospecimen_doesnt_allow_duplicates(self):
        caregiverbio_one = CaregiverBiospecimen(caregiver_fk=self.first_caregiver,collection_fk=self.serum_one,
                                                status_fk=self.status_outcome_complete,biospecimen_date=datetime.date.today(),
                                                incentive_fk=self.incentive_one)
        with self.assertRaises(ValidationError):
            caregiverbio_one.full_clean()


class ChildBiospecimenModelTest(ModelTest):

    def test_child_links_to_biospecimen(self):
        test_child = Child.objects.filter(childbiospecimen__age_category_fk=self.early_childhood,childbiospecimen__collection_fk=self.urine_six).first()
        self.assertEqual(test_child,self.child_one)

    def test_multiple_children_link_to_one_biospecimen(self):
        urine = ChildBiospecimen.objects.filter(collection_fk=self.urine_six)

        self.assertEqual(urine.count(),2)
