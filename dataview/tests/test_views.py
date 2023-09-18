import logging
import unittest
from django.test import TestCase
from dataview.models import Caregiver,Name,CaregiverName,Address,\
    CaregiverAddress, Email, CaregiverEmail,CaregiverPhone,Phone,SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,SurveyOutcome,CaregiverSurvey,Incentive,IncentiveType,Status,Collection,CaregiverBiospecimen,Mother,Relation,ConsentItem,\
    NonMotherCaregiver, ConsentType,Child, PrimaryCaregiver, HealthcareFacility,Recruitment,ChildName,ChildAddress,ChildSurvey,\
    Assent,ChildAssent,AgeCategory,ChildBiospecimen,Race, Ethnicity
import datetime
from django.utils import timezone
from dataview.forms import CaregiverBiospecimenForm, IncentiveForm
from django.utils.html import escape

logging.basicConfig(level=logging.CRITICAL)

class TestCaseSetup(TestCase):
    def setUp(self):
        self.caucasion = Race.objects.create(race='W')
        self.black = Race.objects.create(race='B')
        self.black = Race.objects.create(race='U')

        self.hispanic = Ethnicity.objects.create(ethnicity='H')
        self.non_hispanic = Ethnicity.objects.create(ethnicity='N')
        self.non_hispanic = Ethnicity.objects.create(ethnicity='U')


        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                        date_of_birth=datetime.date(1985, 7, 3),
                                                        ewcp_participant_identifier='0000',
                                                        participation_level_identifier='01',
                                                        specimen_id='4444', echo_pin='333',
                                                        race_fk=self.caucasion,
                                                        ethnicity_fk=self.hispanic)
        self.second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
                                                         date_of_birth=datetime.date(1985, 7, 4),
                                                         ewcp_participant_identifier='0001',
                                                         participation_level_identifier='02',
                                                         specimen_id='5555', echo_pin='444',
                                                         race_fk=self.black, ethnicity_fk=self.non_hispanic
                                                         )


        self.first_caregiver_name = Name()
        self.first_caregiver_name.first_name = 'Jane'
        self.first_caregiver_name.last_name = 'Doe'
        self.first_caregiver_name.save()

        self.second_caregiver_name = Name()
        self.second_caregiver_name.first_name = 'Jessica'
        self.second_caregiver_name.last_name = 'Smith'
        self.second_caregiver_name.save()

        self.first_caregiver_old_name = Name.objects.create(first_name='Sandy', last_name='Cheeks')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_name, revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_old_name,
                                     revision_number=2,
                                     eff_start_date=timezone.now(), status='A')

        CaregiverName.objects.create(caregiver_fk=self.second_caregiver, name_fk=self.second_caregiver_name,
                                     revision_number=1,
                                     eff_start_date=timezone.now(), status='C')

        # Create address
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

        # Create email
        email = Email.objects.create(email='jharrison12@gmail.com')
        CaregiverEmail.objects.create(email_fk=email, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        email_secondary = Email.objects.create(email='f@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_secondary, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.SECONDARY)

        email_archived = Email.objects.create(email='INACTIVE@gmail.com')
        CaregiverEmail.objects.create(email_fk=email_archived, caregiver_fk=self.first_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.INACTIVE)

        email2 = Email.objects.create(email='jharrison13@gmail.com')
        CaregiverEmail.objects.create(email_fk=email2, caregiver_fk=self.second_caregiver,
                                      email_type=CaregiverEmail.EmailTypeChoices.PRIMARY)

        # Create phone
        phone = Phone.objects.create(area_code='555', phone_number='555-5555')
        CaregiverPhone.objects.create(phone_fk=phone, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.PRIMARY)

        phone_secondary = Phone.objects.create(area_code='666', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_secondary, caregiver_fk=self.first_caregiver,
                                      phone_type=CaregiverPhone.CaregiverPhoneTypeChoices.SECONDARY)

        phone_archived = Phone.objects.create(area_code='777', phone_number='666-6666')
        CaregiverPhone.objects.create(phone_fk=phone_archived, caregiver_fk=self.first_caregiver,
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

        # Create caregiver
        contact_a_email = Email.objects.create(email='b@b.com')
        contact_b_email = Email.objects.create(email='c@c.com')
        contact_c_email = Email.objects.create(email='d@d.com')

        contact_a_name = Name.objects.create(first_name='John', last_name='Jones')
        contact_b_name = Name.objects.create(first_name='Jessica', last_name='Jones')
        contact_c_name = Name.objects.create(first_name='James', last_name='Contact')

        contact_a_address = Address.objects.create(address_line_1='two drive', city='Lansing', state='MI',
                                                   zip_code='38000')
        contact_c_address = Address.objects.create(address_line_1='three drive', city='East Lansing', state='MI',
                                                   zip_code='38000')

        contact_a_phone = Phone.objects.create(area_code='999', phone_number='999-9999')
        contact_b_phone = Phone.objects.create(area_code='999', phone_number='999-9998')
        contact_c_phone = Phone.objects.create(area_code='999', phone_number='999-9997')

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

        #Create surveys


        self.new_project = Project.objects.create(project_name='MARCH')

        self.prenatal_1 = Survey.objects.create(survey_name='Prenatal 1', project_fk=self.new_project)
        self.prenatal_2 = Survey.objects.create(survey_name='Prenatal 2', project_fk=self.new_project)

        self.completed_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Completed')
        self.incomplete_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Incomplete')

        self.incentive_type_one = IncentiveType.objects.create(incentive_type_text='Gift Card')

        self.incentive_one = Incentive.objects.create(incentive_type_fk=self.incentive_type_one,
                                                      incentive_date=datetime.date(2023,8,24), incentive_amount=100)

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date(2023,8,30)
                                                                   )

        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_2,
                                                                   survey_outcome_fk=self.incomplete_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date(2023,8,30)
                                                                   )

        self.caregiver_2_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.second_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_one,
                                                                   survey_completion_date=datetime.date(2023,8,30)
                                                                   )

        #create recruitment
        self.health_care_facility_1 = HealthcareFacility.objects.create(name='University of Michigan')

        self.caregiver_1_recruitment = Recruitment.objects.create(caregiver_fk=self.first_caregiver,
                                                                  incentive_fk=self.incentive_one,
                                                                  healthcare_facility_fk=self.health_care_facility_1,
                                                                  recruitment_date=datetime.date.today())
        # create biospecimen

        self.completed_status = Status.objects.create(status='Completed')
        self.incomplete = Status.objects.create(status='Incomplete')
        self.collected = Status.objects.create(status='Collected')
        self.urine_one = Collection.objects.create(collection_type='Urine', collection_number=1)
        self.urine_two = Collection.objects.create(collection_type='Urine', collection_number=2)
        self.urine_three = Collection.objects.create(collection_type='Urine', collection_number=3)
        self.urine_six = Collection.objects.create(collection_type='Urine', collection_number=6)
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
        self.hair = Collection.objects.create(collection_type='Hair')
        self.toenail_prenatal = Collection.objects.create(collection_type='Toenail', collection_number='Prenatal')
        self.toenail = Collection.objects.create(collection_type='Toenail')
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
            biospecimen_date=datetime.date(2023,8,23))

        self.biospecimen_toenail_prenatal_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.toenail_prenatal,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023,8,26))

        self.biospecimen_salvia_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.saliva,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023,8,26))

        self.biospecimen_placenta_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.collected,
            collection_fk=self.placenta,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023,8,26))

        #create mother and nonmother caregiver tables

        self.mother_in_law = Relation.objects.create(relation_type='Mother-in-law')

        self.mother_one = Mother.objects.create(caregiver_fk=self.first_caregiver,due_date=datetime.date(2021,1,3))
        self.non_mother_one = NonMotherCaregiver.objects.create(caregiver_fk=self.second_caregiver,relation_fk=self.mother_in_law)

        self.primary_care_giver_child_one = PrimaryCaregiver.objects.create(mother_fk=self.mother_one)
        self.primary_care_giver_child_two = PrimaryCaregiver.objects.create(non_mother_caregiver_fk=self.non_mother_one)

        #creat consent item

        self.consent_mother_placenta = ConsentType.objects.create(consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_PLACENTA)
        self.consent_mother_blood = ConsentType.objects.create(consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_BLOOD)
        self.consent_mother_urine = ConsentType.objects.create(consent_type_text=ConsentType.ConsentTypeChoices.MOTHER_URINE)
        self.consent_mother_address = ConsentType.objects.create(consent_type_text=ConsentType.ConsentTypeChoices.ADDRESS)
        self.consent_mother_birth_cert = ConsentType.objects.create(consent_type_text=ConsentType.ConsentTypeChoices.BIRTH_CERTIFICATE)

        self.consent_mother_placenta_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_placenta,caregiver_fk=self.first_caregiver)
        self.consent_mother_blood_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_blood,caregiver_fk=self.first_caregiver)
        self.consent_mother_urine_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_urine,caregiver_fk=self.first_caregiver)
        self.consent_mother_address_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_address,caregiver_fk=self.first_caregiver)
        self.consent_mother_birth_cert_caregiver_one = ConsentItem.objects.create(consent_type_fk=self.consent_mother_birth_cert,caregiver_fk=self.first_caregiver)

        # create child

        self.child_one = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_one,
                                              charm_project_identifier='7000M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.MALE,
                                              birth_date=datetime.date(2020, 7, 3),
                                              child_twin=False,race_fk=self.caucasion, ethnicity_fk=self.hispanic)
        self.child_two = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                              charm_project_identifier='7001M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=datetime.date(2021, 8, 10),
                                              child_twin=False, race_fk=self.black,ethnicity_fk=self.non_hispanic)

        self.child_one_name = Name.objects.create(last_name='Harrison',first_name='Jonathan')
        self.child_two_name = Name.objects.create(last_name='Smith',first_name='Kevin')

        self.child_name_connection = ChildName.objects.create(child_fk=self.child_one,name_fk=self.child_one_name,status=ChildName.ChildNameStatusChoice.CURRENT,)
        self.child_two_name_connection = ChildName.objects.create(child_fk=self.child_two,name_fk=self.child_two_name,status=ChildName.ChildNameStatusChoice.CURRENT,)

        #create child address

        # create child address

        self.child_address = ChildAddress.objects.create(child_fk=self.child_one, address_fk=self.address)

        #create child survey

        self.survey_that_child_takes = Survey.objects.create(survey_name='Eight Year Survey',project_fk=self.new_project)
        self.other_survey_that_child_takes = Survey.objects.create(survey_name='Five Year Survey',project_fk=self.new_project)

        self.child_one_survey_one = ChildSurvey.objects.create(child_fk=self.child_one,
                                                           survey_fk=self.survey_that_child_takes,
                                                           survey_outcome_fk=self.completed_survey_outcome,
                                                           survey_completion_date=datetime.date(2023,9,12))

        self.child_two_survey_one = ChildSurvey.objects.create(child_fk=self.child_two,
                                                           survey_fk=self.other_survey_that_child_takes,
                                                           survey_outcome_fk=self.incomplete_survey_outcome,
                                                           survey_completion_date=datetime.date(2023,9,12))

        #child assent
        self.eight_year_assent = Assent.objects.create(assent_text='Eight Year Survey')
        self.five_year_assent = Assent.objects.create(assent_text='Five Year Survey')
        self.child_one_eight_year_assent = ChildAssent.objects.create(child_fk=self.child_one,
                                                                  assent_fk=self.eight_year_assent,
                                                                  assent_date=datetime.date(2023,9,5),assent_boolean=True)
        self.child_two_five_year_assent = ChildAssent.objects.create(child_fk=self.child_two,
                                                                  assent_fk=self.five_year_assent,
                                                                  assent_date=datetime.date(2023,9,5),assent_boolean=False)

        # child biospecimen
        self.early_childhood = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.EARLY_CHILDHOOD)
        self.child_one_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                           status_fk=self.completed_status,
                                                                           collection_fk=self.urine_six,
                                                                           incentive_fk=self.incentive_one,
                                                                           age_category_fk=self.early_childhood,
                                                                           collection_date=datetime.date(2023, 8, 15),
                                                                           kit_sent_date=datetime.date(2023, 8, 10))

        self.child_two_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_two,
                                                                           status_fk=self.completed_status,
                                                                           collection_fk=self.urine_one,
                                                                           incentive_fk=self.incentive_one,
                                                                           age_category_fk=self.early_childhood,
                                                                           collection_date=datetime.date(2023, 8, 15),
                                                                           kit_sent_date=datetime.date(2023, 8, 10))

        self.child_one_biospecimen_hair = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                          status_fk=self.completed_status,
                                                                          collection_fk=self.hair,
                                                                          incentive_fk=self.incentive_one,
                                                                          age_category_fk=self.early_childhood,
                                                                          collection_date=datetime.date(2023, 8, 15),
                                                                          kit_sent_date=datetime.date(2023, 8, 12))

        self.child_one_biospecimen_toenail = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                             status_fk=self.completed_status,
                                                                             collection_fk=self.toenail,
                                                                             incentive_fk=self.incentive_one,
                                                                             age_category_fk=self.early_childhood,
                                                                             collection_date=datetime.date(2023, 8, 15),
                                                                             kit_sent_date=datetime.date(2023, 8, 12))


# Create your tests here.
class HomePageTest(TestCaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')

class CaregiverPageTest(TestCaseSetup):

    def test_caregiver_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/')
        self.assertTemplateUsed(response, 'dataview/caregiver.html')

    def test_mother_page_contains_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/')
        self.assertContains(response,'P7000')

    def test_mother_page_contains_second_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/')
        self.assertContains(response,'P7001')

    def test_mother_page_contains_biospecimen_page_link(self):
        response = self.client.get(f'/data/caregiver/')
        self.assertContains(response,'Biospecimen')

class CaregiverInformationPageTest(TestCaseSetup):

    def test_caregiver_information_page_uses_correct_template(self):
        response = self.client.get('/data/caregiver/P7000/')
        self.assertTemplateUsed(response,'dataview/caregiver_info.html')

    def test_caregiver_info_page_contains_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'P7000')

    def test_other_caregiver_info_page_contains_other_caregiver_id(self):
        response = self.client.get(f'/data/caregiver/P7001/')
        self.assertNotContains(response,'P7000')
        self.assertContains(response,'P7001')

    def test_caregiver_information_page_contains_birthday(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'July 3, 1985')

    def test_caregiver_information_page_contains_ewcp(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '0000')

    def test_caregiver_information_page_contains_participation_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '01')

    def test_caregiver_information_page_contains_echo_pin(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '333')

    def test_caregiver_information_page_contains_specimen_id(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '4444')

    def test_caregiver_information_page_contains_active_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')

    def test_caregiver_information_page_does_not_contain_archived_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, 'Sandy')
        self.assertNotContains(response, 'Cheeks')

    def test_caregiver_information_page_contains_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'One Drive')

    def test_caregiver_information_page_shows_primary_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'jharrison12@gmail.com')

    def test_caregiver_information_page_shows_secondary_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'f@gmail.com')

    def test_caregiver_information_page_does_not_show_archived_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, 'INACTIVE@gmail.com')

    def test_caregiver_information_page_shows_primary_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '555-555-5555')

    def test_caregiver_information_page_shows_secondary_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, '666-666-6666')

    def test_caregiver_information_page_does_not_show_inactive_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertNotContains(response, '777-666-6666')

    def test_caregiver_information_page_shows_social_media_handle(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Twitter: @jonathan')
        self.assertContains(response,'Facebook: jonathan-h')
        self.assertContains(response,'Instagram: @jonathanscat')

    def test_caregiver_information_page_shows_contact_a_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A First Name: John')
        self.assertContains(response,'Contact A Last Name: Jones')

    def test_caregiver_information_page_shows_contact_a_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Phone Number: 999-999-9999')

    def test_caregiver_information_page_shows_contact_a_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Address: two drive')

    def test_caregiver_information_page_shows_contact_a_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact A Email: b@b.com')

    def test_caregiver_information_page_shows_contact_b_name(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B First Name: Jessica')
        self.assertContains(response,'Contact B Last Name: Jones')

    def test_caregiver_information_page_shows_contact_b_phone(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Phone Number: 999-999-9998')

    def test_caregiver_information_page_shows_contact_b_address(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Address: two drive')

    def test_caregiver_information_page_shows_contact_b_email(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response,'Contact B Email: c@c.com')

    def test_caregiver_information_page_does_not_show_contact_b_if_it_does_not_exist(self):
        response = self.client.get(f'/data/caregiver/P7001/')
        self.assertNotContains(response,'Contact B')


class CaregiverSurveyPageTest(TestCaseSetup):

    def test_caregiver_survey_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertTemplateUsed(response, 'dataview/caregiver_survey.html')

    def test_caregiver_survey_page_shows_prenatal1_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 1: Complete')

    def test_caregiver_survey_page_shows_prenatal2_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 2: Incomplete')

class CaregiverBiospecimenPageTest(TestCaseSetup):

    def test_caregiver_biospecimen_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertTemplateUsed(response,'dataview/caregiver_biospecimen.html')

    def test_caregiver_biospecimen_page_contains_urine_1(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response,'Serum 1: Completed')

    def test_caregiver_b_biospecimen_does_not_appear_in_caregiver_a_page(self):
        response = self.client.get(f'/data/caregiver/P7001/biospecimen/')
        self.assertNotContains(response,'Serum 1: Completed')

    def test_caregiver_a_bio_page_shows_all_urines(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response,"Urine 1")
        self.assertContains(response,"Urine EC")

    def test_caregiver_a_bio_page_shows_hair(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response,"Prenatal Hair: Collected")

    def test_caregiver_a_bio_page_shows_toenails(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response, "Prenatal Toenail: Collected")

    def test_caregiver_a_bio_page_shows_saliva(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response, "Saliva: Collected")

    def test_caregiver_a_bio_page_does_not_show_none_saliva(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertNotContains(response, "None Saliva")

    def test_caregiver_a_bio_page_does_not_show_none_placenta(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertNotContains(response, "None Placenta")

    def test_caregiver_a_bio_page_shows_placenta(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/')
        self.assertContains(response, "Placenta: Collected")

class CaregiverBioSpecimenEntryPage(TestCaseSetup):

    def test_using_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/entry/')
        self.assertTemplateUsed(response, 'dataview/caregiver_biospecimen_entry.html')

    def test_caregiver_bio_entry_page_uses_bio_form(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/entry/')
        self.assertIsInstance(response.context['bio_form'], CaregiverBiospecimenForm)

    def test_bio_entry_redirects_after_post(self):

        response = self.client.post(f'/data/caregiver/P7000/biospecimen/entry/', data={'bio_form-collection_fk':self.placenta_two.pk,
                                                                                       'bio_form-status_fk':self.collected.pk,
                                                                                       'bio_form-biospecimen_date':datetime.date(2023,8,23),
                                                                                       #'incentive_fk':  self.incentive_one.pk,
                                                                                       'bio_form-caregiver_fk': self.first_caregiver.pk,
                                                                                       'incentive_form-incentive_type_fk': self.incentive_one.incentive_type_fk.pk,
                                                                                       'incentive_form-incentive_date':datetime.date(2023,8,23),
                                                                                       'incentive_form-incentive_amount':1,
                                                                                       })

        self.assertRedirects(response,f"/data/caregiver/P7000/biospecimen/")

    def test_unique_validation_errors_are_sent_back_to_entry_page(self):
        response = self.client.post(f'/data/caregiver/P7000/biospecimen/entry/', data={'bio_form-collection_fk':self.placenta.pk,
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

        self.assertTemplateUsed(response, 'dataview/caregiver_biospecimen_entry.html')
        expected_error = escape("This type of biospecimen for this charm id already exists")
        self.assertContains(response, expected_error)


    def test_caregiver_bio_entry_page_uses_incentive_form(self):
        response = self.client.get(f'/data/caregiver/P7000/biospecimen/entry/')
        self.assertIsInstance(response.context['incentive_form'], IncentiveForm)

    def test_bio_entry_is_connected_to_incentive_submitted_in_form(self):

        response = self.client.post(f'/data/caregiver/P7000/biospecimen/entry/', data={'bio_form-collection_fk':self.placenta_two.pk,
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

class CaregiverConsentItemPage(TestCaseSetup):

    def test_caregiver_consent_item_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/consentitem/')
        self.assertTemplateUsed(response,'dataview/caregiver_consent_item.html')

    def test_caregiver_consent_shows_mother_placenta(self):
        response = self.client.get(f'/data/caregiver/P7000/consentitem/')
        self.assertContains(response, "Mother Placenta")

class ChildPage(TestCaseSetup):

    def test_child_page_returns_correct_template(self):
        response = self.client.get(f'/data/child/')
        self.assertTemplateUsed(response,'dataview/child.html')

    def test_child_page_contains_child_id(self):
        response = self.client.get(f'/data/child/')
        self.assertContains(response,'7000M1')

    def test_child_page_contains_information_page(self):
        response = self.client.get(f'/data/child/')
        self.assertContains(response,'Information Page')

    def test_child_page_contains_survey_page(self):
        response = self.client.get(f'/data/child/')
        self.assertContains(response,'Survey Page')

    def test_child_page_contains_assent_page(self):
        response = self.client.get(f'/data/child/')
        self.assertContains(response,'Assent Page')

class ChildInformationPage(TestCaseSetup):

    def test_child_info_page_returns_correct_template(self):
        response = self.client.get(f'/data/child/7000M1/')
        self.assertTemplateUsed(response,'dataview/child_information.html')

    def test_child_information_page_has_name(self):
        response = self.client.get(f'/data/child/7000M1/')
        self.assertContains(response,'Child\'s name is: Harrison, Jonathan')

    def test_child_information_page_has_mother_id(self):
        response = self.client.get(f'/data/child/7000M1/')
        ##TODO figure out how to test for text when using link
        self.assertContains(response,'<a href=/data/caregiver/P7000/> P7000</a>')

    def test_child_information_page_shows_non_mother_caregiver_id(self):
        response = self.client.get(f'/data/child/7001M1/')
        ##TODO figure out how to test for text when using link
        self.assertContains(response,'<a href=/data/caregiver/P7001/> P7001</a>')

    def test_child_information_page_wrong_id_shows_404(self):
        response = self.client.get(f'/data/child/7002M1/')
        self.assertEqual(response.status_code,404)

    def test_child_information_page_shows_relation_if_not_mother(self):
        response = self.client.get(f'/data/child/7001M1/')
        self.assertContains(response,'Relation: Mother-in-law')

    def test_child_information_page_does_not_shows_relation_mother(self):
        response = self.client.get(f'/data/child/7000M1/')
        self.assertNotContains(response,'Relation')

    def test_child_information_page_shows_address(self):
        response = self.client.get(f'/data/child/7000M1/')
        self.assertContains(response,'One Drive')

    def test_child_information_page_shows_address_if_address_associated_with_two_children(self):
        child_three = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                           charm_project_identifier='7002M1',
                                           birth_hospital=self.health_care_facility_1,
                                           birth_sex=Child.BirthSexChoices.FEMALE,
                                           birth_date=datetime.date(2021, 8, 10),
                                           child_twin=False)
        new_child_address = ChildAddress.objects.create(address_fk=self.address, child_fk=child_three)

        response = self.client.get(f'/data/child/7000M1/')
        self.assertContains(response,'One Drive')

class ChildSurveyPage(TestCaseSetup):

    def test_child_survey_page_returns_correct_template(self):
        response = self.client.get(f'/data/child/7000M1/survey/')
        self.assertTemplateUsed(response,'dataview/child_survey.html')

    def test_child_survey_page_has_eight_year_survey(self):
        response = self.client.get(f'/data/child/7000M1/survey/')
        self.assertContains(response, 'Eight Year Survey: Completed')

    def test_other_child_page_shows_other_survey(self):
        response = self.client.get(f'/data/child/7001M1/survey/')
        self.assertContains(response, 'Five Year Survey: Incomplete')

    def test_child_one_survey_page_does_not_show_five_year(self):
        response = self.client.get(f'/data/child/7000M1/survey/')
        self.assertNotContains(response, 'Five Year Survey: Incomplete')

    def test_child_survey_page_does_not_show_incentive_if_it_doesnt_exist(self):
        response = self.client.get(f'/data/child/7000M1/survey/')
        self.assertNotContains(response, 'Incentive')

class ChildAssentPage(TestCaseSetup):

    def test_child_assent_page_uses_correct_template(self):
        response = self.client.get(f'/data/child/7000M1/assent/')
        self.assertTemplateUsed(response,'dataview/child_assent.html')

    def test_child_assent_page_has_header(self):
        response = self.client.get(f'/data/child/7000M1/assent/')
        self.assertContains(response,'Child ID: 7000M1')

    def test_child_assent_page_has_assent(self):
        response = self.client.get(f'/data/child/7000M1/assent/')
        self.assertContains(response,'Eight Year Survey: True')

    def test_that_child_one_page_doesnt_contain_five_year(self):
        response = self.client.get(f'/data/child/7000M1/assent/')
        self.assertNotContains(response, 'Five Year Survey')

    def test_that_other_child_assent_page_doesnt_contain_Eight_Year(self):
        response = self.client.get(f'/data/child/7001M1/assent/')
        self.assertNotContains(response, 'Eight Year Survey')

    def test_child_assent_page_wrong_id_shows_404(self):
        response = self.client.get(f'/data/child/7002M1/')
        self.assertEqual(response.status_code,404)

class ChildBiospecimenPage(TestCaseSetup):

    def test_child_biospecimen_page_uses_correct_template(self):
        response = self.client.get(f'/data/child/7000M1/biospecimen/')
        self.assertTemplateUsed(response,'dataview/child_biospecimen.html')

    def test_child_biospecimen_page_has_header(self):
        response = self.client.get(f"/data/child/7000M1/biospecimen/")
        self.assertContains(response,'Child ID: 7000M1')

    def test_child_biospecimen_page_has_urine(self):
        response = self.client.get(f"/data/child/7000M1/biospecimen/")
        self.assertContains(response,'Urine 6: Completed')

    def test_child_biospecimen_contains_all_child_biospecimens(self):
        response = self.client.get(f"/data/child/7000M1/biospecimen/")
        child_bios = ChildBiospecimen.objects.values('collection_fk__collection_type')
        logging.critical(child_bios)
        child_bios_list = list(set(value for dic in child_bios for value in dic.values()))
        logging.critical(child_bios_list)
        for value in child_bios_list:
            self.assertContains(response, value)