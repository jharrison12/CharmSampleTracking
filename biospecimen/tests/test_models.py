import logging
import sqlite3

from django.test import TestCase
from biospecimen.models import Collection,CaregiverBiospecimen,ChildBiospecimen,Status,Processed,Outcome,Stored,Shipped,\
    Received,Collected,Trimester,Perinatal,NotCollected,NoConsent,ShippedWSU,ShippedECHO,KitSent
import datetime
from dataview.models import Caregiver,Incentive,Child,User
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
                                                status_fk=self.status_outcome_processed_complete_one, biospecimen_date=datetime.date.today(),
                                                incentive_fk=self.incentive_one)
        with self.assertRaises(ValidationError):
            caregiverbio_one.full_clean()

    def test_caregiver_biospecimen_outcome_links_to_processed(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots',project_fk__project_name__contains='ECHO1')
        outcome = Outcome.objects.get(processed__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_stored(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots',project_fk__project_name__contains='ECHO1')
        stored = Stored.objects.create()
        outcome = Outcome.objects.get(stored__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_shipped(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots',project_fk__project_name__contains='ECHO1')

        outcome = Outcome.objects.get(shipped__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_outcome_links_to_received(self):
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk__collection_type_fk__collection_type='Bloodspots',project_fk__project_name__contains='ECHO1')
        outcome = Outcome.objects.get(received__status__caregiverbiospecimen=caregiver)
        self.assertEqual(outcome.get_outcome_display(),'Completed')

    def test_caregiver_biospecimen_links_to_collected(self):
        caregiver_bio = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier='P7000',
                                                         trimester_fk__trimester='F',
                                                         collection_fk__collection_type_fk__collection_type='Bloodspots').first()
        caregiver = Caregiver.objects.get(caregiverbiospecimen__status_fk__collected_fk__number_of_tubes=5)
        self.assertEqual(caregiver,caregiver_bio.caregiver_fk)

    def test_caregiver_biospecimen_links_to_trimester(self):
        urine_tree = Collection.objects.get(collection_number_fk__collection_number=None,collection_type_fk__collection_type='Urine')
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk=urine_tree,status_fk__collected_fk=None)
        trimester = Trimester.objects.get(trimester='S')
        self.assertEqual(caregiver.trimester_fk,trimester)

    def test_caregiver_biospecimen_outcome_links_to_perinatal(self):
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta',collection_number_fk=None)
        caregiver = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',collection_fk=placenta)
        perinatal_event = Perinatal.objects.get(child_fk__charm_project_identifier='7000M1')
        self.assertEqual(caregiver.perinatal_fk,perinatal_event)

    def test_caregiver_biospecimen_outcome_links_to_not_collected(self):
        not_collected = NotCollected.objects.create()
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta', collection_number_fk=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',
                                                     collection_fk=placenta)
        status_nc = Status.objects.create(not_collected_fk=not_collected)
        caregiver_bio.status_fk = status_nc
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.not_collected_fk,not_collected)

    def test_caregiver_biospecimen_outcome_links_to_no_consent(self):
        no_consent = NoConsent.objects.create()
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta', collection_number_fk=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',
                                                     collection_fk=placenta)
        status_no_consent = Status.objects.create(no_consent_fk=no_consent)
        caregiver_bio.status_fk = status_no_consent
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.no_consent_fk,no_consent)

    def test_caregiver_biospecimen_links_to_shippedwsu(self):
        shipped_wsu = ShippedWSU.objects.create(shipped_by=User.objects.get(pk=1))
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta', collection_number_fk=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',
                                                     collection_fk=placenta)
        status_shipped_wsu = Status.objects.create(shipped_wsu_fk=shipped_wsu)
        caregiver_bio.status_fk = status_shipped_wsu
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.shipped_wsu_fk,shipped_wsu)


    def test_caregiver_biospecimen_links_to_shipped_eccho(self):
        shipped_echo = ShippedECHO.objects.create()
        placenta = Collection.objects.get(collection_type_fk__collection_type='Placenta', collection_number_fk=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='P7000',
                                                         collection_fk=placenta)
        status_shipped_echo = Status.objects.create(shipped_echo_fk=shipped_echo)
        caregiver_bio.status_fk = status_shipped_echo
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.shipped_echo_fk, shipped_echo)

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

class KitSentModelTest(DatabaseSetup):

    def test_child_links_to_kit(self):
        child_urine_one_z_to_f = ChildBiospecimen.objects.get(collection_fk__collection_type_fk__collection_type='Urine',child_fk__charm_project_identifier='7002M1')
        kit_sent = KitSent.objects.create(kit_sent_date=timezone.datetime(2023,5,5,12,0,0,))
        status_kit_sent = Status.objects.create(kit_sent_fk=kit_sent)
        child_urine_one_z_to_f.status_fk=status_kit_sent
        child_urine_one_z_to_f.save()
        self.assertEqual(child_urine_one_z_to_f.status_fk.kit_sent_fk.kit_sent_date, timezone.datetime(2023,5,5,12,0,0,))


