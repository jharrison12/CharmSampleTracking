import logging
import sqlite3

from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,CaregiverSurvey,Incentive,IncentiveType,SurveyOutcome,HealthcareFacility,Recruitment,ConsentVersion,\
    ConsentContract,CaregiverSocialMediaHistory,Mother,NonPrimaryCaregiver,Relation,PrimaryCaregiver, ConsentItem, ConsentType,Child,ChildName,ChildAddress,ChildAddressHistory,\
    ChildSurvey,ChildAssent,Assent,AgeCategory,Race, Ethnicity,Pregnancy, CaregiverChildRelation
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Processed,Outcome
from dataview.tests.db_setup import DatabaseSetup
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

logging.basicConfig(level=logging.DEBUG)

class CaregiverModelsTest(DatabaseSetup):

    def test_saving_and_retrieving_caregiver(self):
        saved_caregivers = Caregiver.objects.all()
        self.assertEqual(saved_caregivers.count(), 5)

        first_saved_caregiver = saved_caregivers[0]
        second_saved_caregiver = saved_caregivers[1]
        self.assertEqual(first_saved_caregiver.charm_project_identifier, 'P7000')
        self.assertEqual(first_saved_caregiver.date_of_birth,datetime.date(1985, 7, 3))
        self.assertEqual(first_saved_caregiver.ewcp_participant_identifier,'0000')
        self.assertEqual(first_saved_caregiver.echo_pin,'333')
        self.assertEqual(second_saved_caregiver.charm_project_identifier, 'P7001')
        self.assertEqual(second_saved_caregiver.date_of_birth,datetime.date(1985, 7, 4))

    def test_caregiver_links_to_race(self):
        caregiver_one = Caregiver.objects.get(charm_project_identifier='P7000')
        self.assertEqual(caregiver_one.race_fk.race,'W')

    def test_caregiver_links_to_ethnicity(self):
        caregiver_one = Caregiver.objects.get(charm_project_identifier='P7000')
        self.assertEqual(caregiver_one.ethnicity_fk.ethnicity,'H')

class CaregiverNameModelsTest(DatabaseSetup):

    def test_caregiver_links_to_name_class(self):
        first_name = Name.objects.create(first_name='Jane',last_name='Doe')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver,name_fk=first_name,revision_number=1,eff_start_date=timezone.now(),status=CaregiverName.CaregiverNameStatusChoice.CURRENT)

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(caregiver_one,self.first_caregiver)

        caregiver_test = Caregiver.objects.filter(caregivername__name_fk__first_name='Jane').first()

        self.assertEqual(caregiver_test,caregiver_one)


    def test_caregiver_name_can_hold_current_name_archived_name(self):
        second_name = Name.objects.create(first_name='Jon',last_name='Smith')
        first_name = Name.objects.create(first_name='Jane',last_name='Doe')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver,name_fk=first_name,revision_number=1,eff_start_date=timezone.now(),status=CaregiverName.CaregiverNameStatusChoice.CURRENT)

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=second_name, revision_number=2,
                                     eff_start_date=timezone.now(), status=CaregiverName.CaregiverNameStatusChoice.ARCHIVED)

        caregiver_one = Caregiver.objects.first()

        caregiver_test = Caregiver.objects.filter(caregivername__name_fk__first_name='Jane').first()

        self.assertEqual(caregiver_test, caregiver_one)

        caregiver_archived = Caregiver.objects.filter(caregivername__name_fk__first_name='Jon').first()

        self.assertEqual(caregiver_archived, caregiver_one)

class CaregiverAddressModelsTest(DatabaseSetup):

    def test_caregiver_links_to_address_class(self):
        caregiver_address_test =Caregiver.objects.filter(caregiveraddress__address_fk__address_line_1='One Drive').first()

        self.assertEqual(self.first_caregiver,caregiver_address_test)




class CaregiverEmailModelsTest(DatabaseSetup):

    def test_email_links_to_caregiver(self):
        caregiver_email_test = Caregiver.objects.filter(caregiveremail__email_fk__email__contains='jharrison').first()

        self.assertEqual(caregiver_email_test,self.first_caregiver)

    def test_caregiver_email_holds_primary_secondary_email(self):
        caregiver_email_test_sd = Caregiver.objects.filter(caregiveremail__email_type='SD').first()

        self.assertEqual(caregiver_email_test_sd, self.first_caregiver)

class CaregiverPhoneModelsTest(DatabaseSetup):

    def test_caregiver_phone_links_to_caregiver(self):
        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_fk__phone_number__contains='555').first()

        self.assertEqual(self.first_caregiver,caregiver_phone_test)

    def test_caregiver_phone_holds_primary_inactive(self):

        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_type='IN').first()

        self.assertEqual(self.first_caregiver,caregiver_phone_test)

class CaregiverSocialMediaModelsTest(DatabaseSetup):

    def test_caregiver_social_media_links_to_caregiver(self):

        first_caregiver_twitter = Caregiver.objects.filter(caregiversocialmedia__social_media_user_name='@jonathan').first()

        self.assertEqual(first_caregiver_twitter,self.first_caregiver)

class CaregiverSocialMediaHistoryModelsTest(DatabaseSetup):

    def test_insert_into_social_media_history_works(self):
        first_row_of_social_media_history = CaregiverSocialMediaHistory.\
            objects.create(caregiver_social_media_fk=self.first_caregiver_social_media,
                           caregiver_fk=self.first_caregiver_social_media.caregiver_fk,
                           social_media_fk=self.first_caregiver_social_media.social_media_fk,
                           social_media_user_name=self.first_caregiver_social_media.social_media_user_name,
                           social_media_consent=self.first_caregiver_social_media.social_media_consent,
                           revision_number=1,
                           revision_date=datetime.date.today()
                           )
        self.assertEqual(first_row_of_social_media_history.social_media_user_name,'@jonathan')

class CaregiverPersonalContactModelsTest(DatabaseSetup):

    def test_personal_contact_a_connects_to_caregiver(self):

        testing_caregiver_a = Caregiver.objects.filter(caregiverpersonalcontact__address_fk__address_line_1='two drive').first()

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(testing_caregiver_a,caregiver_one)

    def test_personal_contact_b_connects_to_caregiver(self):

        testing_caregiver_a = Caregiver.objects.filter(caregiverpersonalcontact__phone_fk__phone_number='999-9999').first()

        caregiver_one = Caregiver.objects.first()

        self.assertEqual(testing_caregiver_a,caregiver_one)

    def test_caregiver_a_has_two_personal_contacts(self):
        caregiver_one = Caregiver.objects.first()
        personal_contacts = CaregiverPersonalContact.objects.filter(caregiver_fk=caregiver_one)

        self.assertEqual(personal_contacts.count(),2)

class CaregiverSurveyModelsTest(DatabaseSetup):

    def test_survey_associated_with_project(self):
        test_survey = Survey.objects.filter().first()
        survey_filter = Survey.objects.filter(project_fk__project_name='MARCH').first()
        self.assertEqual(test_survey,survey_filter)

    def test_survey_can_be_asscociated_with_two_caregivers(self):
        survey_filter = Survey.objects.get(caregiversurvey__caregiver_fk=self.second_caregiver)
        self.assertEqual(survey_filter.survey_name,'Prenatal 1')

    def test_there_are_two_survey_one_rows(self):
        survey_filter = CaregiverSurvey.objects.filter(survey_fk__survey_name='Prenatal 1')
        self.assertEqual(survey_filter.count(),2)

class RecruitmentModelsTest(DatabaseSetup):

    def test_health_care_facility_connects_to_recruitment(self):
        hospital = HealthcareFacility.objects.filter(recruitment__caregiver_fk=self.first_caregiver).first()
        self.assertEqual(self.health_care_facility_1,hospital)

class ConsentVersionModelsTest(DatabaseSetup):

    def test_caregiver_can_have_multiple_consent_contract(self):
        number_of_consents = ConsentContract.objects.filter(caregiver_fk=self.first_caregiver)
        self.assertEqual(number_of_consents.count(),2)

    def test_you_can_pull_latest_consent(self):
        latest_consent = ConsentContract.objects.latest('consent_date')
        self.assertEqual(latest_consent.consent_date,datetime.date.today())

    def test_consents_can_have_multiple_caregivers(self):
        number_of_consent_signed = ConsentContract.objects.filter(consent_version_fk=self.consent_version_1).all()
        self.assertEqual(number_of_consent_signed.count(),2)

class CaregiverMotherModelsTest(DatabaseSetup):
    def test_caregiver_links_to_mother_table(self):
        mother_table_row = Mother.objects.filter(caregiver_fk=self.first_caregiver).first()
        mother_table_row_2 = Mother.objects.create(caregiver_fk=self.second_caregiver)
        self.assertNotEqual(mother_table_row_2,mother_table_row)

class CaregiverMotherPregnancyTest(DatabaseSetup):

    def test_pregnancy_links_to_mother(self):
        mother_one_test = Caregiver.objects.filter(mother__pregnancy=self.mother_one_pregnancy_one).first()
        self.assertEqual(mother_one_test,self.first_caregiver)

    def test_save_gestational_age_works(self):
        #didn't work in test db
        right_gest_age = str(( datetime.date.today() - self.mother_one_pregnancy_one.last_menstrual_period).days // 7)
        self.assertEqual(right_gest_age,self.mother_one_pregnancy_one.calculate_gestational_age())

    def test_gest_age_stops_calculating_at_birth(self):
        #TODO why does this return 2 children???
        # child_from_pregnancy_one = Child.objects.get(pregnancy_fk__child__charm_project_identifier='7000M1')
        child_from_pregnancy_one = Child.objects.get(charm_project_identifier='7000M1')

        last_menstrual = self.mother_one_pregnancy_one.last_menstrual_period
        date_of_birth = child_from_pregnancy_one.birth_date
        gest_age = str((date_of_birth - last_menstrual).days//7)
        self.mother_one_pregnancy_one.save()
        self.assertEqual(gest_age,
                         self.mother_one_pregnancy_one.gestational_age_at_birth)

class CaregiverChildRelationDatabaseSetup(DatabaseSetup):
    def test_non_mother_caregiver_links_to_caregiver_table(self):
        non_pcg_row = CaregiverChildRelation.objects.filter(caregiver_fk=self.second_caregiver).first()
        self.assertEqual(non_pcg_row.relation_fk.relation_type,'Mother-in-law')

class PrimaryCaregiverModelsTest(DatabaseSetup):

    def test_primary_caregiver_links_to_caregiver_table(self):
        self.assertEqual(self.primary_care_giver_child_one.caregiver_fk,self.first_caregiver)

    def test_primary_caregiver_links_to_non_caregiver_table(self):
        self.assertEqual(self.primary_care_giver_child_two.caregiver_fk,self.second_caregiver)

class ConsentItemDatabaseSetup(DatabaseSetup):

    def test_that_consent_item_links_to_caregiver(self):
        first_caregiver_placenta = Caregiver.objects.filter(consentitem__consent_type_fk__consent_type_text="MTHR_PLCNT").first()
        self.assertEqual(first_caregiver_placenta,self.first_caregiver)

class ChildDatabaseSetup(DatabaseSetup):

    def test_child_links_to_only_one_caregiver(self):
        caregiver_one = self.first_caregiver
        caregiver_one_through_child = Caregiver.objects.get(primarycaregiver__child=self.child_one)
        self.assertEqual(caregiver_one,caregiver_one_through_child)

    def test_different_child_links_to_non_primary_caregiver(self):
        caregiver_two_through_child = Caregiver.objects.get(primarycaregiver__child=self.child_two)
        self.assertEqual(self.second_caregiver,caregiver_two_through_child)

    def test_is_mother_model_function_works_for_non_mother(self):
        self.assertEqual(self.child_two.is_caregiver_mother(),False)

    def test_is_mother_model_function_works_for_mother(self):
        self.assertEqual(self.child_one.is_caregiver_mother(),True)


class ChildNameDatabaseSetup(DatabaseSetup):

    def test_child_name_links_to_child(self):
        child_object = Child.objects.filter(childname__name_fk__last_name='Harrison').first()
        self.assertEqual(child_object,self.child_one)

class ChildAddressDatabaseSetup(DatabaseSetup):

    def test_child_address_links_to_child(self):
        child_object = Child.objects.filter(childaddress__address_fk__address_line_1='One Drive').first()
        self.assertEqual(child_object, self.child_one)

    def test_child_address_links_to_second_child(self):
        new_primary_caregiver = PrimaryCaregiver.objects.create(caregiver_fk=self.first_caregiver)
        child_three = Child.objects.create(primary_care_giver_fk=new_primary_caregiver,
                                              charm_project_identifier='7003M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=datetime.date(2021, 8, 10),
                                              child_twin=False,pregnancy_fk=self.mother_one_pregnancy_one)
        new_child_address = ChildAddress.objects.create(address_fk=self.address,child_fk=child_three)

        child_addresses = ChildAddress.objects.filter(address_fk__address_line_1='One Drive')
        self.assertEqual(child_addresses.count(),2)

    def test_child_address_history_links_to_child_address(self):
        child_address_history = ChildAddressHistory.objects.create(child_address_fk=self.child_address,
                                                                   child_fk=self.child_one,
                                                                   address_fk=self.address,
                                                                   revision_number=0,
                                                                   revision_date=datetime.date.today()
                                                                )
        child_one_test = Child.objects.get(childaddresshistory__child_address_fk__address_fk=self.address)
        self.assertEqual(child_one_test,self.child_one)


class ChildSurveyDatabaseSetup(DatabaseSetup):

    def test_child_survey_links_to_child(self):
        child_test = Child.objects.get(childsurvey__survey_outcome_fk__survey_outcome_text='Completed')

        self.assertEqual(child_test,self.child_one)

    def test_child_survey_links_to_two_children(self):
        child_survey_test = ChildSurvey.objects.create(child_fk=self.child_two,
                                                           survey_fk=self.survey_that_child_takes,
                                                           survey_outcome_fk=self.completed_survey_outcome,
                                                           survey_completion_date=datetime.date(2023, 9, 13))

        number_of_surveys = ChildSurvey.objects.filter(survey_fk=self.survey_that_child_takes)

        self.assertEqual(number_of_surveys.count(),2)


class ChildAssentDatabaseSetup(DatabaseSetup):

    def test_child_assent_links_to_child(self):
        test_child = Child.objects.get(childassent__assent_fk=self.eight_year_assent)
        self.assertEqual(self.child_one,test_child)

    def test_child_assent_primary_key_works(self):
        dup_child_assent = ChildAssent(assent_fk=self.eight_year_assent,child_fk=self.child_one)
        with self.assertRaises(ValidationError):
            dup_child_assent.full_clean()


