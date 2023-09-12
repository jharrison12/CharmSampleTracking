import logging
import sqlite3

from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    AddressMove,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,CaregiverSurvey,Incentive,IncentiveType,SurveyOutcome,HealthcareFacility,Recruitment,ConsentVersion,\
    ConsentContract,CaregiverSocialMediaHistory,CaregiverAddressHistory,Mother,NonMotherCaregiver,Relation, Status,\
    CaregiverBiospecimen,Collection,PrimaryCaregiver, ConsentItem, ConsentType,Child,ChildName,ChildAddress
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

logging.basicConfig(level=logging.DEBUG)

class ModelTest(TestCase):
    def setUp(self):
        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                        date_of_birth=datetime.date(1985, 7, 3),
                                                        ewcp_participant_identifier='0000',
                                                        participation_level_identifier='01',
                                                        specimen_id='4444', echo_pin='333')
        self.second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
                                                         date_of_birth=datetime.date(1985, 7, 4),
                                                         ewcp_participant_identifier='0001',
                                                         participation_level_identifier='02',
                                                         specimen_id='5555', echo_pin='444')

        self.first_caregiver_name = Name()
        self.first_caregiver_name.first_name = 'Jane'
        self.first_caregiver_name.last_name = 'Doe'
        self.first_caregiver_name.save()

        self.second_caregiver_name = Name()
        self.second_caregiver_name.first_name = 'Jessica'
        self.second_caregiver_name.last_name = 'Smith'
        self.second_caregiver_name.save()

        self.first_caregiver_old_name = Name.objects.create(first_name='Sandy', last_name='Cheeks')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_name,revision_number=1,eff_start_date = timezone.now(), status = 'C')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_old_name,revision_number = 2,eff_start_date = timezone.now(), status = 'A')

        CaregiverName.objects.create(caregiver_fk=self.second_caregiver, name_fk=self.second_caregiver_name,revision_number = 1,eff_start_date = timezone.now(), status = 'C')


        #create address
        self.address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        self.address_move = Address.objects.create(address_line_1='future street', address_line_2='apt 1',
                                                   city='Lansing', state='MI', zip_code='38000')

        self.caregiver_1_address = CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver,
                                                                   address_fk=self.address)
        self.caregiver_1_address_move = CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver,
                                                                        address_fk=self.address_move)

        self.address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        self.caregiver_2_address = CaregiverAddress.objects.create(caregiver_fk=self.second_caregiver,
                                                                   address_fk=self.address2)

        #create email
        self.email = Email.objects.create(email='jharrison12@gmail.com')
        self.email_secondary = Email.objects.create(email='f@gmail.com')

        CaregiverEmail.objects.create(caregiver_fk=self.first_caregiver,
                                      email_fk=self.email,email_type = CaregiverEmail.EmailTypeChoices.PRIMARY)

        CaregiverEmail.objects.create(caregiver_fk=self.first_caregiver,
                                      email_fk=self.email_secondary,
                                      email_type = CaregiverEmail.EmailTypeChoices.SECONDARY)
        #create phone

        self.phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        self.phone_two = Phone.objects.create(area_code='666', phone_number='666-6666')
        self.phone_inactive = Phone.objects.create(area_code='888', phone_number='888-8888')

        CaregiverPhone.objects.create(caregiver_fk=self.first_caregiver, phone_fk=self.phone,
                                               phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)
        CaregiverPhone.objects.create(caregiver_fk=self.first_caregiver, phone_fk=self.phone_two,
                                               phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)
        CaregiverPhone.objects.create(caregiver_fk=self.first_caregiver, phone_fk=self.phone_inactive,
                                               phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.INACTIVE)

        # Create social media
        twitter = SocialMedia.objects.create(social_media_name='Twitter')
        self.first_caregiver_social_media = CaregiverSocialMedia.objects.create(social_media_fk=twitter, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='@jonathan',social_media_consent=True)
        facebook = SocialMedia.objects.create(social_media_name='Facebook')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='jonathan-h', social_media_consent=True)
        facebook = SocialMedia.objects.create(social_media_name='Instagram')
        CaregiverSocialMedia.objects.create(social_media_fk=facebook, caregiver_fk=self.first_caregiver,
                                            social_media_user_name='@jonathanscat',social_media_consent=True)

        #create contact
        contact_a_name = Name.objects.create(first_name='John', last_name='Jones')
        contact_b_name = Name.objects.create(first_name='Jessica', last_name='Jones')
        contact_c_name = Name.objects.create(first_name='James', last_name='Contact')

        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')
        contact_c_email = Email.objects.create(email='d@d.com')

        contact_a_phone = Phone.objects.create(area_code='999', phone_number='999-9999')
        contact_b_phone = Phone.objects.create(area_code='999', phone_number='999-9998')
        contact_c_phone = Phone.objects.create(area_code='999', phone_number='999-9997')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI',
                                                    zip_code='38000')
        contact_c_address = Address.objects.create(address_line_1='three drive', city='East Lansing', state='MI',
                                                   zip_code='38000')


        self.caregiver_contact_a = CaregiverPersonalContact.objects.create(caregiver_fk=self.first_caregiver,
                                                                           name_fk=contact_a_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_a_email,
                                                                           phone_fk=contact_a_phone,
                                                                           caregiver_contact_type='PR')

        self.caregiver_contact_b = CaregiverPersonalContact.objects.create(caregiver_fk=self.first_caregiver,
                                                                           name_fk=contact_b_name,
                                                                           address_fk=contact_a_address,
                                                                           email_fk=contact_b_email,
                                                                           phone_fk=contact_b_phone,
                                                                           caregiver_contact_type='SD')

        self.caregiver_contact_b = CaregiverPersonalContact.objects.create(caregiver_fk=self.second_caregiver,
                                                                           name_fk=contact_c_name,
                                                                           address_fk=contact_c_address,
                                                                           email_fk=contact_c_email,
                                                                           phone_fk=contact_c_phone,
                                                                           caregiver_contact_type='PR')

        # Create surveys

        self.new_project = Project.objects.create(project_name='MARCH')

        self.prenatal_1 = Survey.objects.create(survey_name='Prenatal 1', project_fk=self.new_project)
        self.prenatal_2 = Survey.objects.create(survey_name='Prenatal 2', project_fk=self.new_project)

        self.completed_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Completed')
        self.incomplete_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Incomplete')

        self.incentive_type_one = IncentiveType.objects.create(incentive_type_text='Gift Card')

        self.incentive_one = Incentive.objects.create(incentive_type_fk=self.incentive_type_one,
                                                      incentive_date=datetime.date(2023, 8, 24), incentive_amount=100)

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_2,
                                                                   survey_outcome_fk=self.incomplete_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        self.caregiver_2_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.second_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date.today()
                                                                   )

        # create recruitment
        self.health_care_facility_1 = HealthcareFacility.objects.create(name='University of Michigan')

        self.caregiver_1_recruitment = Recruitment.objects.create(caregiver_fk=self.first_caregiver,
                                                                  incentive_fk=self.incentive_one,
                                                                  healthcare_facility_fk=self.health_care_facility_1,
                                                                  recruitment_date=datetime.date.today())

        #Create consent
        self.consent_version_1 = ConsentVersion.objects.create(consent_version='5.1')
        self.consent_version_2 = ConsentVersion.objects.create(consent_version='5.2')
        self.consent_contract_1 = ConsentContract.objects.create(caregiver_fk=self.first_caregiver,
                                                                 consent_version_fk=self.consent_version_1,
                                                                 consent_date=datetime.date.today() - datetime.timedelta(days=1))
        self.consent_contract_1 = ConsentContract.objects.create(caregiver_fk=self.first_caregiver,
                                                                 consent_version_fk=self.consent_version_2,
                                                                 consent_date=datetime.date.today())
        self.consent_contract_1_cg_2 = ConsentContract.objects.create(caregiver_fk=self.second_caregiver,
                                                                      consent_version_fk=self.consent_version_1,
                                                                      consent_date=datetime.date.today())

        # create biospecimen

        self.completed_status = Status.objects.create(status='Completed')
        self.incomplete = Status.objects.create(status='Incomplete')
        self.collected = Status.objects.create(status='Collected')
        self.urine_one = Collection.objects.create(collection_type='Urine', collection_number=1)
        self.urine_two = Collection.objects.create(collection_type='Urine', collection_number=2)
        self.urine_three = Collection.objects.create(collection_type='Urine', collection_number=3)
        self.urine_ec = Collection.objects.create(collection_type='Urine', collection_number='EC')
        self.urine_mc = Collection.objects.create(collection_type='Urine', collection_number='MC')
        self.serum_one = Collection.objects.create(collection_type='Serum', collection_number=1)
        self.serum_two = Collection.objects.create(collection_type='Serum', collection_number=2)
        self.plasma_one = Collection.objects.create(collection_type='Plasma', collection_number=1)
        self.plasma_two = Collection.objects.create(collection_type='Plasma', collection_number=2)
        self.bloodspots_one = Collection.objects.create(collection_type='Bloodspots', collection_number=1)
        self.bloodspots_two = Collection.objects.create(collection_type='Bloodspots', collection_number=2)
        self.whole_blood_one = Collection.objects.create(collection_type='Whole Blood', collection_number=1)
        self.whole_blood_two = Collection.objects.create(collection_type='Whole Blood', collection_number=2)
        self.buffy_coat_one = Collection.objects.create(collection_type='Buffy Coat', collection_number=1)
        self.buffy_coat_two = Collection.objects.create(collection_type='Buffy Coat', collection_number=2)
        self.red_blood_cells_one = Collection.objects.create(collection_type='Red Blood Cells', collection_number=1)
        self.red_blood_cells_two = Collection.objects.create(collection_type='Red Blood Cells', collection_number=2)
        self.hair_prenatal = Collection.objects.create(collection_type='Hair', collection_number='Prenatal')
        self.toenail_prenatal = Collection.objects.create(collection_type='Toenail', collection_number='Prenatal')
        self.saliva = Collection.objects.create(collection_type='Saliva')
        self.placenta = Collection.objects.create(collection_type='Placenta')
        self.placenta_two = Collection.objects.create(collection_type='Placenta', collection_number=2)

        self.biospecimen_urine_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.urine_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_urine_one_caregiver_two = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.second_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.urine_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_urine_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.urine_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_urine_three_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.urine_three,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_urine_ec_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                      status_fk=self.incomplete,
                                                                                      collection_fk=self.urine_ec,
                                                                                      incentive_fk=self.incentive_one,
                                                                                      biospecimen_date=datetime.date.today())

        self.biospecimen_urine_mc_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                      status_fk=self.incomplete,
                                                                                      collection_fk=self.urine_mc,
                                                                                      incentive_fk=self.incentive_one,
                                                                                      biospecimen_date=datetime.date.today())

        self.biospecimen_serum_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.serum_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 23))

        self.biospecimen_serum_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.serum_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_plasma_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.plasma_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.plasma_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_bloodspots_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.bloodspots_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_bloodspots_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.bloodspots_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_whole_blood_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.whole_blood_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_whole_blood_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.whole_blood_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_buffy_coat_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.buffy_coat_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_buffy_coat_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.buffy_coat_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_red_blood_cells_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.completed_status,
            collection_fk=self.red_blood_cells_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_red_blood_cells_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.incomplete,
            collection_fk=self.red_blood_cells_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today())

        self.biospecimen_hair_prenatal_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.hair_prenatal,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 23))

        self.biospecimen_toenail_prenatal_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.toenail_prenatal,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 26))

        self.biospecimen_salvia_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.saliva,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 26))

        self.biospecimen_placenta_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.placenta,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 26))

        # create mother and nonmother caregiver tables

        self.mother_in_law = Relation.objects.create(relation_type='Mother-in-law')

        self.mother_one = Mother.objects.create(caregiver_fk=self.first_caregiver, due_date=datetime.date(2021, 1, 3))
        self.non_mother_one = NonMotherCaregiver.objects.create(caregiver_fk=self.second_caregiver,
                                                                relation_fk=self.mother_in_law)

        self.primary_care_giver_child_one = PrimaryCaregiver.objects.create(mother_fk=self.mother_one)
        self.primary_care_giver_child_two = PrimaryCaregiver.objects.create(non_mother_caregiver_fk=self.non_mother_one)

        # creat consent item

        self.consent_mother_placenta = ConsentType.objects.create(
            consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_PLACENTA)
        self.consent_mother_blood = ConsentType.objects.create(
            consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_BLOOD)
        self.consent_mother_urine = ConsentType.objects.create(
            consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_URINE)
        self.consent_mother_address = ConsentType.objects.create(
            consent_type_text=ConsentType.ConsentTypeChoices.ADDRESS)
        self.consent_mother_birth_cert = ConsentType.objects.create(
            consent_type_text=ConsentType.ConsentTypeChoices.BIRTH_CERTIFICATE)

        self.consent_mother_placenta_caregiver_one = ConsentItem.objects.create(
            consent_type_fk=self.consent_mother_placenta, caregiver_fk=self.first_caregiver)
        self.consent_mother_blood_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_blood,
                                                                             caregiver_fk=self.first_caregiver)
        self.consent_mother_urine_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_urine,
                                                                             caregiver_fk=self.first_caregiver)
        self.consent_mother_address_caregiver_one = ConsentItem.objects.create(
            consent_type_fk=self.consent_mother_address, caregiver_fk=self.first_caregiver)
        self.consent_mother_birth_cert_caregiver_one = ConsentItem.objects.create(
            consent_type_fk=self.consent_mother_birth_cert, caregiver_fk=self.first_caregiver)

        # create child

        self.child_one = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_one,
                                              charm_project_identifier='7000M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.MALE,
                                              birth_date=datetime.date(2020, 7, 3),
                                              child_twin=False)
        self.child_two = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                              charm_project_identifier='7001M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=datetime.date(2021, 8, 10),
                                              child_twin=False)

        self.child_one_name = Name.objects.create(last_name='Harrison', first_name='Jonathan')
        self.child_two_name = Name.objects.create(last_name='Smith', first_name='Kevin')

        self.child_name_connection = ChildName.objects.create(child_fk=self.child_one, name_fk=self.child_one_name,
                                                              status=ChildName.ChildNameStatusChoice.CURRENT, )
        self.child_two_name_connection = ChildName.objects.create(child_fk=self.child_two, name_fk=self.child_two_name,
                                                                  status=ChildName.ChildNameStatusChoice.CURRENT, )

        #create child address

        self.child_address = ChildAddress.objects.create(child_fk=self.child_one,address_fk=self.address)

class CaregiverModelsTest(ModelTest):

    def test_saving_and_retrieving_caregiver(self):
        saved_caregivers = Caregiver.objects.all()
        self.assertEqual(saved_caregivers.count(), 2)

        first_saved_caregiver = saved_caregivers[0]
        second_saved_caregiver = saved_caregivers[1]
        self.assertEqual(first_saved_caregiver.charm_project_identifier, 'P7000')
        self.assertEqual(first_saved_caregiver.date_of_birth,datetime.date(1985, 7, 3))
        self.assertEqual(first_saved_caregiver.ewcp_participant_identifier,'0000')
        self.assertEqual(first_saved_caregiver.echo_pin,'333')
        self.assertEqual(second_saved_caregiver.charm_project_identifier, 'P7001')
        self.assertEqual(second_saved_caregiver.date_of_birth,datetime.date(1985, 7, 4))

class CaregiverNameModelsTest(ModelTest):

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

class CaregiverAddressModelsTest(ModelTest):

    def test_caregiver_links_to_address_class(self):
        caregiver_address_test =Caregiver.objects.filter(caregiveraddress__address_fk__address_line_1='One Drive').first()

        self.assertEqual(self.first_caregiver,caregiver_address_test)

    def test_caregiver_address_move_works(self):
        one_caregiver_address = AddressMove.objects.create(address_fk=self.address_move,address_move_date=datetime.date.today())

        caregiver_address_test_move =Caregiver.objects.filter(caregiveraddress__address_fk__addressmove=one_caregiver_address).first()

        self.assertEqual(self.first_caregiver,caregiver_address_test_move)

class CaregiverAddressHistoryModelsTest(ModelTest):
    def test_insert_into_address_history_works(self):
        first_row_of_address_history = CaregiverAddressHistory.objects.create(caregiver_address_fk=self.caregiver_1_address,
                                                                              caregiver_fk=self.caregiver_1_address.caregiver_fk,
                                                                              address_fk=self.caregiver_1_address.address_fk,
                                                                              revision_number=1,
                                                                              revision_date=datetime.date.today())

        self.assertEqual(first_row_of_address_history.address_fk.address_line_1,'One Drive')

class CaregiverEmailModelsTest(ModelTest):

    def test_email_links_to_caregiver(self):
        caregiver_email_test = Caregiver.objects.filter(caregiveremail__email_fk__email__contains='jharrison').first()

        self.assertEqual(caregiver_email_test,self.first_caregiver)

    def test_caregiver_email_holds_primary_secondary_email(self):
        caregiver_email_test_sd = Caregiver.objects.filter(caregiveremail__email_type='SD').first()

        self.assertEqual(caregiver_email_test_sd, self.first_caregiver)

class CaregiverPhoneModelsTest(ModelTest):

    def test_caregiver_phone_links_to_caregiver(self):
        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_fk__phone_number__contains='555').first()

        self.assertEqual(self.first_caregiver,caregiver_phone_test)

    def test_caregiver_phone_holds_primary_inactive(self):

        caregiver_phone_test = Caregiver.objects.filter(caregiverphone__phone_type='IN').first()

        self.assertEqual(self.first_caregiver,caregiver_phone_test)

class CaregiverSocialMediaModelsTest(ModelTest):

    def test_caregiver_social_media_links_to_caregiver(self):

        first_caregiver_twitter = Caregiver.objects.filter(caregiversocialmedia__social_media_user_name='@jonathan').first()

        self.assertEqual(first_caregiver_twitter,self.first_caregiver)

class CaregiverSocialMediaHistoryModelsTest(ModelTest):

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

class CaregiverPersonalContactModelsTest(ModelTest):

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

class CaregiverSurveyModelsTest(ModelTest):

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

class RecruitmentModelsTest(ModelTest):

    def test_health_care_facility_connects_to_recruitment(self):
        hospital = HealthcareFacility.objects.filter(recruitment__caregiver_fk=self.first_caregiver).first()
        self.assertEqual(self.health_care_facility_1,hospital)

class ConsentVersionModelsTest(ModelTest):

    def test_caregiver_can_have_multiple_consent_contract(self):
        number_of_consents = ConsentContract.objects.filter(caregiver_fk=self.first_caregiver)
        self.assertEqual(number_of_consents.count(),2)

    def test_you_can_pull_latest_consent(self):
        latest_consent = ConsentContract.objects.latest('consent_date')
        self.assertEqual(latest_consent.consent_date,datetime.date.today())

    def test_consents_can_have_multiple_caregivers(self):
        number_of_consent_signed = ConsentContract.objects.filter(consent_version_fk=self.consent_version_1).all()
        self.assertEqual(number_of_consent_signed.count(),2)

class CaregiverMotherModelsTest(ModelTest):
    def test_caregiver_links_to_mother_table(self):
        mother_table_row = Mother.objects.filter(caregiver_fk=self.first_caregiver).first()
        mother_table_row_2 = Mother.objects.create(caregiver_fk=self.second_caregiver,due_date=datetime.date(2020,7,3))
        self.assertNotEqual(mother_table_row_2,mother_table_row)

class NonMotherCaregiverModelsTest(ModelTest):
    def test_non_mother_caregiver_links_to_caregiver_table(self):
        non_mother_table_row = NonMotherCaregiver.objects.filter(caregiver_fk=self.second_caregiver).first()
        self.assertEqual(non_mother_table_row.relation_fk.relation_type,'Mother-in-law')

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
                                                status_fk=self.completed_status,biospecimen_date=datetime.date.today(),
                                                incentive_fk=self.incentive_one)
        with self.assertRaises(ValidationError):
            caregiverbio_one.full_clean()

class PrimaryCaregiverModelsTest(ModelTest):

    def test_primary_caregiver_links_to_caregiver_table(self):
        self.assertEqual(self.primary_care_giver_child_one.mother_fk.caregiver_fk,self.first_caregiver)

    def test_primary_caregiver_links_to_non_caregiver_table(self):
        self.assertEqual(self.primary_care_giver_child_two.non_mother_caregiver_fk.caregiver_fk,self.second_caregiver)

class ConsentItemModelTest(ModelTest):

    def test_that_consent_item_links_to_caregiver(self):
        first_caregiver_placenta = Caregiver.objects.filter(consentitem__consent_type_fk__consent_type_text="MTHR_PLCNT").first()
        self.assertEqual(first_caregiver_placenta,self.first_caregiver)

class ChildModelTest(ModelTest):

    def test_child_links_to_only_one_caregiver(self):
        caregiver_one = self.first_caregiver
        caregiver_one_through_child = Caregiver.objects.get(mother__primarycaregiver__child=self.child_one)
        self.assertEqual(caregiver_one,caregiver_one_through_child)

    def test_different_child_links_to_non_primary_caregiver(self):
        caregiver_two_through_child = Caregiver.objects.get(nonmothercaregiver__primarycaregiver__child=self.child_two)
        self.assertEqual(self.second_caregiver,caregiver_two_through_child)

    def test_is_mother_model_function_works_for_non_mother(self):
        self.assertEqual(self.child_two.is_caregiver_mother(),False)

    def test_is_mother_model_function_works_for_mother(self):
        self.assertEqual(self.child_one.is_caregiver_mother(),True)

    def test_primary_caregiver_table_cannot_have_mother_fk_and_non_mother_fk_on_same_row(self):
        third_caregiver = Caregiver.objects.create(charm_project_identifier='P7003',
                                                        date_of_birth=datetime.date(1985,7,3),
                                                        ewcp_participant_identifier='0000',
                                                        participation_level_identifier='01',
                                                        specimen_id='7777',
                                                        echo_pin='333')
        fourth_caregiver = Caregiver.objects.create(charm_project_identifier='P7004',
                                                         date_of_birth=datetime.date(1985,7,4),
                                                         ewcp_participant_identifier='0001',
                                                         participation_level_identifier='02',
                                                         specimen_id='6666',
                                                         echo_pin='444')

        new_mother = Mother.objects.create(caregiver_fk=third_caregiver,due_date=datetime.date(2023,7,3))
        new_non_mother = NonMotherCaregiver.objects.create(caregiver_fk=fourth_caregiver,relation_fk=self.mother_in_law)


        primary_care_giver_one = PrimaryCaregiver(mother_fk=new_mother,non_mother_caregiver_fk=new_non_mother)
        with self.assertRaises(ValidationError):
            primary_care_giver_one.full_clean()


class ChildNameModelTest(ModelTest):

    def test_child_name_links_to_child(self):
        child_object = Child.objects.filter(childname__name_fk__last_name='Harrison').first()
        self.assertEqual(child_object,self.child_one)

class ChildAddressModelTest(ModelTest):

    def test_child_address_links_to_child(self):
        child_object = Child.objects.filter(childaddress__address_fk__address_line_1='One Drive').first()
        self.assertEqual(child_object, self.child_one)

    def test_child_address_links_to_second_child(self):
        child_three = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                              charm_project_identifier='7002M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=datetime.date(2021, 8, 10),
                                              child_twin=False)
        new_child_address = ChildAddress.objects.create(address_fk=self.address,child_fk=child_three)

        child_addresses = ChildAddress.objects.filter(address_fk__address_line_1='One Drive')
        self.assertEqual(child_addresses.count(),2)