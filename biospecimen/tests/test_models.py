import logging

from biospecimen.models import Collection,CaregiverBiospecimen,ChildBiospecimen,Status,\
    PregnancyTrimester,NotCollected,NoConsent,ShippedWSU,ShippedECHO,KitSent,Declined,ReceivedWSU,\
    ShippedMSU,ReceivedMSU,Caregiver,Incentive,Child,User,Component
import datetime
from biospecimen.tests.db_setup import DatabaseSetup
from django.utils import timezone
from django.core.exceptions import ValidationError

class BioSpecimenCaregiverModelsTest(DatabaseSetup):

    def blood_received_at_wsu(self,primary_key):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/received_wsu/post/',
                                    data={'received_at_wsu_form-received_date_time': timezone.datetime(2023, 12, 5, 5, 5, 5)})

        return response

    def test_biospecimen_urine_links_to_two_caregivers(self):
        urine_samples = CaregiverBiospecimen.objects.filter(collection_fk__collection_type='U')
        self.assertEqual(urine_samples.count(),8)

    def test_biospecimen_links_to_incentive_table(self):
        caregiverbio_one = CaregiverBiospecimen.objects.get(caregiver_fk=Caregiver.objects.get(charm_project_identifier='4100'),
                                                collection_fk=Collection.objects.get(collection_type='U'),trimester_fk__trimester='S')
        caregiverbio_one.incentive_fk = Incentive.objects.create(incentive_amount=100)
        caregiverbio_one.save()

        self.assertEqual(caregiverbio_one.incentive_fk.incentive_amount,100)

    def test_caregiver_biospecimen_doesnt_allow_duplicates(self):
        caregiverbio_one = CaregiverBiospecimen(caregiver_fk=Caregiver.objects.get(charm_project_identifier='4100'),
                                                collection_fk=Collection.objects.get(collection_type='U'))
        with self.assertRaises(ValidationError):
            caregiverbio_one.full_clean()


    def test_caregiver_biospecimen_links_to_component(self):
        caregiver_bio = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier='4100',
                                                         trimester_fk__trimester='S',
                                                         component__component_type='S').first()
        component_to_pull = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,component_type='S')
        self.assertEqual(caregiver_bio,component_to_pull.caregiver_biospecimen_fk)

    def test_caregiver_biospecimen_links_to_trimester(self):
        caregiver = Caregiver.objects.get(charm_project_identifier='4100')
        caregiverbio = CaregiverBiospecimen.objects.get(biospecimen_id='12UR410001')
        trimester = PregnancyTrimester.objects.get(pregnancy_fk__caregiver_fk=caregiver, pregnancy_fk__pregnancy_number=1,trimester='S')

        self.assertEqual(caregiverbio.trimester_fk,trimester)

    def test_caregiver_biospecimen_outcome_links_to_not_collected(self):
        not_collected = NotCollected.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_nc = Status.objects.create(not_collected_fk=not_collected)
        caregiver_bio.status_fk = status_nc
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.not_collected_fk,not_collected)

    def test_caregiver_biospecimen_outcome_links_to_no_consent(self):
        no_consent = NoConsent.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_no_consent = Status.objects.create(no_consent_fk=no_consent)
        caregiver_bio.status_fk = status_no_consent
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.no_consent_fk,no_consent)

    def test_caregiver_biospecimen_links_to_shippedwsu(self):
        shipped_wsu = ShippedWSU.objects.create(shipped_by=User.objects.get(username='staff'))
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_shipped_wsu = Status.objects.create(shipped_wsu_fk=shipped_wsu)
        caregiver_bio.status_fk = status_shipped_wsu
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.shipped_wsu_fk,shipped_wsu)


    def test_caregiver_biospecimen_links_to_shipped_echo(self):
        shipped_echo = ShippedECHO.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_shipped_echo = Status.objects.create(shipped_echo_fk=shipped_echo)
        caregiver_bio.status_fk = status_shipped_echo
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.shipped_echo_fk, shipped_echo)

    def test_caregiver_biospecimen_links_to_declined(self):
        declined = Declined.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_declined = Status.objects.create(declined_fk=declined)
        caregiver_bio.status_fk = status_declined
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.declined_fk,declined)

    def test_caregiver_biospecimen_links_to_shipped_msu(self):
        shipped_msu = ShippedMSU.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_shipped_msu = Status.objects.create(shipped_msu_fk=shipped_msu)
        caregiver_bio.status_fk = status_shipped_msu
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.shipped_msu_fk, shipped_msu)

    def test_caregiver_biospecimen_links_to_received_msu(self):
        received_msu = ReceivedMSU.objects.create()
        placenta = Collection.objects.get(collection_type='C', collection_number=None)
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=placenta,project_fk__project_name__contains='ECHO2')
        status_received_msu = Status.objects.create(received_msu_fk=received_msu)
        caregiver_bio.status_fk = status_received_msu
        caregiver_bio.save()
        self.assertEqual(caregiver_bio.status_fk.received_msu_fk, received_msu)

class ChildBiospecimenModelTest(DatabaseSetup):

    def test_child_links_to_biospecimen(self):
        urine = Collection.objects.get(collection_type='U')
        test_child = Child.objects.filter(childbiospecimen__age_category_fk__age_category='ZF',
                                          childbiospecimen__collection_fk=urine).first()
        self.assertEqual(test_child.charm_project_identifier,'4100F1')

    def test_multiple_children_link_to_one_biospecimen(self):
        urine = Collection.objects.get(collection_type='U')
        urine = ChildBiospecimen.objects.filter(collection_fk=urine)
        self.assertEqual(urine.count(),2)

class KitSentModelTest(DatabaseSetup):

    def test_child_links_to_kit(self):
        child_urine_one_z_to_f = ChildBiospecimen.objects.get(collection_fk__collection_type='U',child_fk__charm_project_identifier='4100F1',age_category_fk__age_category='ZF')
        kit_sent = KitSent.objects.create(kit_sent_date=timezone.datetime(2023,5,5,12,0,0,))
        status_kit_sent = Status.objects.create(kit_sent_fk=kit_sent)
        child_urine_one_z_to_f.status_fk=status_kit_sent
        child_urine_one_z_to_f.save()
        self.assertEqual(child_urine_one_z_to_f.status_fk.kit_sent_fk.kit_sent_date, timezone.datetime(2023,5,5,12,0,0,))


class ReceivedWSUModelTest(DatabaseSetup):

    def test_child_bio_links_to_received_wsu(self):
        child_urine_one_z_to_f = ChildBiospecimen.objects.get(collection_fk__collection_type='U',child_fk__charm_project_identifier='4100F1',age_category_fk__age_category='ZF')
        received_at_wsu = ReceivedWSU.objects.create(received_date_time=timezone.datetime(2023,5,7,12,0,0,))
        status_received_wsu = Status.objects.create(received_wsu_fk=received_at_wsu)
        child_urine_one_z_to_f.status_fk=status_received_wsu
        child_urine_one_z_to_f.save()
        self.assertEqual(child_urine_one_z_to_f.status_fk.received_wsu_fk.received_date_time, timezone.datetime(2023,5,7,12,0,0,))

class ComponentBioModelTest(DatabaseSetup):


    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester, project='ECHO2'):
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project)
        return caregiverbio.pk

    def blood_collected_form_send(self, primary_key, type, false_or_true):
        response = self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/post/', data={f'blood_form-{type}': false_or_true,
                                                                                              f'blood_form-{type}_number_of_tubes': 5,
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

    def blood_shipped_to_wsu(self,primary_key):
        response =  self.client.post(f'/biospecimen/caregiver/4100/{primary_key}/shipped_wsu/post/',
                                    data={'shipped_to_wsu_form-shipped_date_and_time': timezone.datetime(2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-tracking_number':555,
                                          'shipped_to_wsu_form-number_of_tubes':5,
                                          'shipped_to_wsu_form-logged_date_time': timezone.datetime(
                                                  2023, 12, 5, 5, 5, 5),
                                          'shipped_to_wsu_form-courier': 'F'})

        return response

    def test_component_links_to_blood_bio(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio, caregiver_biospecimen_fk__trimester_fk__trimester='S',component_type='S')
        self.assertEqual(caregiver_bio,component_test.caregiver_biospecimen_fk)

    def test_component_links_to_collected(self):
        primary_key = self.return_caregiver_bio_pk('4100', 'B', 'S')
        self.blood_initial_send_form(primary_key, 'C')
        self.blood_collected_form_send(primary_key,'serum',false_or_true=True)
        blood = Collection.objects.get(collection_type='B')
        caregiver_bio = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier='4100',
                                                         collection_fk=blood,project_fk__project_name__contains='ECHO2',trimester_fk__trimester='S')
        component_test = Component.objects.get(caregiver_biospecimen_fk=caregiver_bio,
                                               caregiver_biospecimen_fk__trimester_fk__trimester='S',
                                               component_type=Component.ComponentType.SERUM)
        test_status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
        component_test.collected_fk=test_status.collected_fk
        component_test.save()
        logging.debug(component_test)
        logging.debug(Status.objects.get(caregiverbiospecimen=caregiver_bio))
        self.assertEqual(component_test.collected_fk, caregiver_bio.status_fk.collected_fk)
