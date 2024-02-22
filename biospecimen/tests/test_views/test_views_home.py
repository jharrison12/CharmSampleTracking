import logging
import unittest
from biospecimen.models import Collection, Status, ChildBiospecimen, CaregiverBiospecimen,\
    ShippedECHO, Collected, Caregiver, Project, Child,User,Component,PregnancyTrimester
import datetime
from django.utils import timezone
from biospecimen.forms import IncentiveForm, ProcessedBiospecimenForm, StoredBiospecimenForm, \
    ShippedBiospecimenForm, CollectedBiospecimenUrineForm, InitialBioForm, ShippedChoiceForm, \
    ShippedtoWSUForm, ShippedtoEchoForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm, \
    ShippedChoiceEchoForm,CollectedChildBloodSpotForm,CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,InitialBioFormChildTooth,\
    CollectedChildToothForm,DeclinedForm,ReceivedatWSUForm,ShippedtoMSUForm,CollectedBiospecimenHairSalivaForm
from biospecimen.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)


class CaregiverEcho2BiospecimenHome(DatabaseSetup):

    def return_caregiver_bio_pk(self, charm_id, collection_type, trimester,age_category=None, project='ECHO2'):
        logging.debug(f"chrarm_id {charm_id} collection_type {collection_type} trimester {trimester} age_category {age_category} project {project}")
        mother_one = Caregiver.objects.get(charm_project_identifier=charm_id)
        caregiverbio = CaregiverBiospecimen.objects.get(caregiver_fk=mother_one,
                                                        collection_fk__collection_type=collection_type,
                                                        trimester_fk__trimester=trimester,
                                                        project_fk__project_name=project,
                                                        age_category_fk__age_category=age_category)

        return caregiverbio.pk

    #TEMPLATES

    def test_charm_identifiers_shows_charm_identifiers_template(self):
        response = self.client.get(f'/biospecimen/charm_ids/')
        self.assertTemplateUsed(response, 'biospecimen/charm_identifiers.html')

    def test_charm_identifiers_shows_charm_identifiers_template(self):
        response = self.client.get(f'/biospecimen/charm_ids/')
        self.assertContains(response,'4100')

    def test_charm_identifiers_4100_pageshows_biospecimen_ids_template(self):
        response = self.client.get(f'/biospecimen/charm_ids/4100/')
        self.assertTemplateUsed(response, 'biospecimen/list_of_mother_bio_ids.html')

class UserTypeChecks(DatabaseSetup):

    def test_user_detroit_cannot_see_flint_participant(self):
        response = self.client.get(f'/biospecimen/charm_ids/')
        self.assertNotContains(response,'4400')

    #REDIRECTS


    #FORMS