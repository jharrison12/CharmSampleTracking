from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dataview.models import Caregiver, Name, CaregiverName, Address, \
    CaregiverAddress, Email, CaregiverEmail, CaregiverPhone, Phone, SocialMedia, CaregiverSocialMedia, \
    CaregiverPersonalContact, \
    Project, Survey, SurveyOutcome, CaregiverSurvey, Incentive, IncentiveType, Status, Collection, CaregiverBiospecimen, \
    Mother, Relation, ConsentItem, ConsentType, Child, PrimaryCaregiver, HealthcareFacility, Recruitment, ChildName, \
    ConsentContract, ConsentVersion, \
    ChildAddress, ChildSurvey, Assent, ChildAssent, AgeCategory, ChildBiospecimen, Race, Ethnicity, Pregnancy, \
    CaregiverChildRelation
import datetime
import time
from django.utils import timezone
import os

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            return
        #create caregiver
        self.caucasion = Race.objects.create(race=Race.RaceChoice.WHITE)
        self.black = Race.objects.create(race=Race.RaceChoice.BLACK)
        self.black = Race.objects.create(race=Race.RaceChoice.UNKNOWN)

        self.hispanic = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.HISPANIC)
        self.non_hispanic = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.NON_HISPANIC)
        self.hispanic_unknown = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.UNKNOWN)


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

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_name,revision_number=1,eff_start_date = timezone.now(), status = 'C')

        CaregiverName.objects.create(caregiver_fk=self.first_caregiver, name_fk=self.first_caregiver_old_name,revision_number = 2,eff_start_date = timezone.now(), status = 'A')

        CaregiverName.objects.create(caregiver_fk=self.second_caregiver, name_fk=self.second_caregiver_name,revision_number = 1,eff_start_date = timezone.now(), status = 'C')

        #create address
        self.address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        self.address_move = Address.objects.create(address_line_1='future street', address_line_2='apt 1',
                                                            city='Lansing', state='MI', zip_code='38000')

        self.caregiver_1_address = CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver, address_fk=self.address)
        self.caregiver_1_address_move = CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver, address_fk=self.address_move)

        self.address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        self.caregiver_2_address = CaregiverAddress.objects.create(caregiver_fk=self.second_caregiver, address_fk=self.address2)

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

        self.mother_one = Mother.objects.create(caregiver_fk=self.first_caregiver)
        self.mother_one_pregnancy_one = Pregnancy.objects.create(mother_fk=self.mother_one,
                                                                 pregnancy_id=f"{self.mother_one.caregiver_fk.charm_project_identifier}F",
                                                                 due_date=datetime.date(2023, 5, 4),
                                                                 last_menstrual_period=datetime.date(2023, 3, 3),
                                                                 )
        self.mother_one_pregnancy_one.save()
        # self.non_mother_one = NonMotherCaregiver.objects.create(caregiver_fk=self.second_caregiver,
        #                                                         relation_fk=self.mother_in_law)

        self.primary_care_giver_child_one = PrimaryCaregiver.objects.create(caregiver_fk=self.first_caregiver)
        self.primary_care_giver_child_two = PrimaryCaregiver.objects.create(caregiver_fk=self.second_caregiver)

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
                                              birth_date=datetime.date(2023, 5, 20),
                                              child_twin=False,race_fk=self.caucasion,
                                              ethnicity_fk=self.hispanic,pregnancy_fk=self.mother_one_pregnancy_one)
        self.mother_one_pregnancy_one.save()
        self.child_two = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                              charm_project_identifier='7001M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=datetime.date(2021, 8, 10),
                                              child_twin=False, race_fk=self.black,ethnicity_fk=self.non_hispanic,pregnancy_fk=self.mother_one_pregnancy_one)

        self.child_one_name = Name.objects.create(last_name='Harrison', first_name='Jonathan')
        self.child_two_name = Name.objects.create(last_name='Smith', first_name='Kevin')

        self.child_name_connection = ChildName.objects.create(child_fk=self.child_one, name_fk=self.child_one_name,
                                                              status=ChildName.ChildNameStatusChoice.CURRENT, )
        self.child_two_name_connection = ChildName.objects.create(child_fk=self.child_two, name_fk=self.child_two_name,
                                                                  status=ChildName.ChildNameStatusChoice.CURRENT, )
        self.second_caregiver_is_mother_in_law = CaregiverChildRelation.objects.create(child_fk=self.child_two,
                                                                                       caregiver_fk=self.second_caregiver,
                                                                                       relation_fk=self.mother_in_law)

        #create child address

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

    def tearDown(self):
        self.browser.quit()

