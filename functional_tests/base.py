from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,CaregiverSurvey,Incentive,IncentiveType,SurveyOutcome,HealthcareFacility,Recruitment,ConsentVersion,\
    ConsentContract,CaregiverSocialMediaHistory,Mother,NonPrimaryCaregiver,Relation,PrimaryCaregiver, ConsentItem, ConsentType,Child,ChildName,ChildAddress,ChildAddressHistory,\
    ChildSurvey,ChildAssent,Assent,AgeCategory,Race, Ethnicity,Pregnancy, CaregiverChildRelation, User
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Processed,Stored,Outcome,Shipped,\
    CollectionType,CollectionNumber,Received,Collected,Trimester,Perinatal,ShippedWSU,ShippedECHO,KitSent
import datetime,pytz
from selenium.webdriver.common.by import By
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

        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.test_user = User.objects.create_user(**self.credentials)
        self.browser.get(self.live_server_url)
        self.browser.get(f'{self.browser.current_url}/accounts/login/')
        username = self.browser.find_element(By.ID,'id_username')
        username.send_keys('testuser')
        password = self.browser.find_element(By.ID,'id_password')
        password.send_keys('secret')
        login = self.browser.find_element(By.ID,'login_button')
        login.click()



        self.caucasion = Race.objects.create(race=Race.RaceChoice.WHITE)
        self.black = Race.objects.create(race=Race.RaceChoice.BLACK)
        self.black = Race.objects.create(race=Race.RaceChoice.UNKNOWN)

        self.hispanic = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.HISPANIC)
        self.non_hispanic = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.NON_HISPANIC)
        self.hispanic_unknown = Ethnicity.objects.create(ethnicity=Ethnicity.EthnicityChoice.UNKNOWN)

        self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
                                                        date_of_birth=timezone.datetime(1985, 7, 3).date(),
                                                        ewcp_participant_identifier='0000',
                                                        participation_level_identifier='01',
                                                        specimen_id='4444', echo_pin='333',
                                                        race_fk=self.caucasion,
                                                        ethnicity_fk=self.hispanic)

        self.second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
                                                         date_of_birth=timezone.datetime(1985, 7, 4).date(),
                                                         ewcp_participant_identifier='0001',
                                                         participation_level_identifier='02',
                                                         specimen_id='5555', echo_pin='444',
                                                         race_fk=self.black, ethnicity_fk=self.non_hispanic
                                                         )

        self.third_caregiver = Caregiver.objects.create(charm_project_identifier='P7002',
                                                        date_of_birth=timezone.datetime(1985, 7, 4).date(),
                                                        ewcp_participant_identifier='0002',
                                                        participation_level_identifier='02',
                                                        specimen_id='6666', echo_pin='555',
                                                        race_fk=self.black, ethnicity_fk=self.non_hispanic
                                                        )

        self.fourth_caregiver = Caregiver.objects.create(charm_project_identifier='P7003',
                                                         date_of_birth=timezone.datetime(1985, 7, 4).date(),
                                                         ewcp_participant_identifier='0003',
                                                         participation_level_identifier='02',
                                                         specimen_id='7777', echo_pin='666',
                                                         race_fk=self.black, ethnicity_fk=self.non_hispanic
                                                         )

        self.fifth_caregiver = Caregiver.objects.create(charm_project_identifier='P7004',
                                                        date_of_birth=timezone.datetime(1985, 7, 4).date(),
                                                        ewcp_participant_identifier='0004',
                                                        participation_level_identifier='02',
                                                        specimen_id='8888', echo_pin='777',
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

        #create incentive
        self.incentive_type_one = IncentiveType.objects.create(incentive_type_text='Gift Card')

        self.incentive_one = Incentive.objects.create(incentive_type_fk=self.incentive_type_one,incentive_amount=100)
        self.incentive_two = Incentive.objects.create(incentive_type_fk=self.incentive_type_one,incentive_amount=100,incentive_date=timezone.datetime(2023, 8, 4).date())

        #create recruitment
        self.health_care_facility_1 = HealthcareFacility.objects.create(name='University of Michigan')

        self.caregiver_1_recruitment = Recruitment.objects.create(caregiver_fk=self.first_caregiver,
                                                                  incentive_fk=self.incentive_one,
                                                                  healthcare_facility_fk=self.health_care_facility_1,
                                                                  recruitment_date=timezone.datetime(2023, 8, 4).date())

        #create mother and nonmother caregiver tables

        self.mother_in_law = Relation.objects.create(relation_type='Mother-in-law')

        self.mother_one = Mother.objects.create(caregiver_fk=self.first_caregiver)
        self.mother_one_pregnancy_one = Pregnancy.objects.create(mother_fk=self.mother_one,
                                                                 pregnancy_id=f"{self.mother_one.caregiver_fk.charm_project_identifier}F",
                                                                 due_date=timezone.datetime(2023, 5, 23).date(),
                                                                 last_menstrual_period=timezone.datetime(2023, 5, 4).date(),
                                                                 )
        self.mother_one_pregnancy_one.save()

        # create trimester

        self.first_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.FIRST,pregnancy_fk=self.mother_one_pregnancy_one)
        self.second_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.SECOND,pregnancy_fk=self.mother_one_pregnancy_one)
        self.third_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.THIRD,pregnancy_fk=self.mother_one_pregnancy_one)

        self.early_childhood_age_category = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.EARLY_CHILDHOOD)
        self.zero_to_five_age_category = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.ZERO_TO_FIVE)
        self.twelve_to_thirteen_months = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.TWELVE_TO_THIRTEEN_MONTHS)
        self.six_to_ten_years = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.SIX_TO_TEN_YEARS)

        #create primary care_giver

        self.primary_care_giver_child_one = PrimaryCaregiver.objects.create(caregiver_fk=self.first_caregiver)
        self.primary_care_giver_child_two = PrimaryCaregiver.objects.create(caregiver_fk=self.second_caregiver)
        self.primary_care_giver_child_three = PrimaryCaregiver.objects.create(caregiver_fk=self.second_caregiver)

        # create child

        self.child_one = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_one,
                                              charm_project_identifier='7000M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.MALE,
                                              birth_date=timezone.datetime(2023, 5, 20).date(),
                                              child_twin=False, race_fk=self.caucasion, ethnicity_fk=self.hispanic,
                                              pregnancy_fk=self.mother_one_pregnancy_one)
        self.mother_one_pregnancy_one.save()
        self.child_two = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_two,
                                              charm_project_identifier='7001M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=timezone.datetime(2021, 8, 10),
                                              child_twin=False, race_fk=self.black, ethnicity_fk=self.non_hispanic,
                                              pregnancy_fk=self.mother_one_pregnancy_one)

        self.child_three = Child.objects.create(primary_care_giver_fk=self.primary_care_giver_child_three,
                                              charm_project_identifier='7002M1',
                                              birth_hospital=self.health_care_facility_1,
                                              birth_sex=Child.BirthSexChoices.FEMALE,
                                              birth_date=timezone.datetime(2021, 8, 10),
                                              child_twin=False, race_fk=self.black, ethnicity_fk=self.non_hispanic,
                                              pregnancy_fk=self.mother_one_pregnancy_one)


        self.child_one_name = Name.objects.create(last_name='Harrison', first_name='Jonathan')
        self.child_two_name = Name.objects.create(last_name='Smith', first_name='Kevin')

        self.child_name_connection = ChildName.objects.create(child_fk=self.child_one, name_fk=self.child_one_name,
                                                              status=ChildName.ChildNameStatusChoice.CURRENT, )
        self.child_two_name_connection = ChildName.objects.create(child_fk=self.child_two, name_fk=self.child_two_name,
                                                                  status=ChildName.ChildNameStatusChoice.CURRENT, )
        self.second_caregiver_is_mother_in_law = CaregiverChildRelation.objects.create(child_fk=self.child_two,
                                                                                       caregiver_fk=self.second_caregiver,
                                                                                       relation_fk=self.mother_in_law)



        # Create address
        self.address = Address.objects.create(address_line_1='One Drive', city='Lansing', state='MI', zip_code='38000')
        self.address_move = Address.objects.create(address_line_1='future street', address_line_2='apt 1',
                                                   city='Lansing', state='MI', zip_code='38000')

        self.caregiver_1_address = CaregiverAddress.objects.create(caregiver_fk=self.first_caregiver,
                                                                   address_fk=self.address,
                                                                   status='C')


        self.address2 = Address.objects.create(address_line_1='Two Drive', city='Lansing', state='MI', zip_code='38000')
        self.caregiver_2_address = CaregiverAddress.objects.create(caregiver_fk=self.second_caregiver,
                                                                   address_fk=self.address2,
                                                                   status='C')

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
        self.echo1 = Project.objects.create(project_name='ECHO1')
        self.echo2 = Project.objects.create(project_name='ECHO2')

        self.prenatal_1 = Survey.objects.create(survey_name='Prenatal 1', project_fk=self.new_project)
        self.prenatal_2 = Survey.objects.create(survey_name='Prenatal 2', project_fk=self.new_project)

        self.completed_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Completed')
        self.incomplete_survey_outcome = SurveyOutcome.objects.create(survey_outcome_text='Incomplete')



        self.caregiver_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_1,
                                                                   survey_outcome_fk=self.completed_survey_outcome,
                                                                   incentive_fk=self.incentive_two,
                                                                   survey_completion_date=timezone.datetime(2023,8,30).date()
                                                                   )

        self.caregiver_prenatal_2 = CaregiverSurvey.objects.create(caregiver_fk=self.first_caregiver,
                                                                   survey_fk=self.prenatal_2,
                                                                   survey_outcome_fk=self.incomplete_survey_outcome,
                                                                   incentive_fk=self.incentive_two,
                                                                   survey_completion_date=timezone.datetime(2023,5,3).date()
                                                                   )

        self.caregiver_2_prenatal_1 = CaregiverSurvey.objects.create(caregiver_fk=self.second_caregiver,
                                                                     survey_fk=self.prenatal_1,
                                                                     survey_outcome_fk=self.completed_survey_outcome,
                                                                     incentive_fk=self.incentive_two,
                                                                     survey_completion_date=timezone.datetime(2023,5,3).date()
                                                                     )



        # Create consent
        self.consent_version_1 = ConsentVersion.objects.create(consent_version='5.1')
        self.consent_version_2 = ConsentVersion.objects.create(consent_version='5.2')
        self.consent_contract_1 = ConsentContract.objects.create(caregiver_fk=self.first_caregiver,
                                                                 consent_version_fk=self.consent_version_1,
                                                                 consent_date=datetime.date.today() - datetime.timedelta(
                                                                     days=1))
        self.consent_contract_1 = ConsentContract.objects.create(caregiver_fk=self.first_caregiver,
                                                                 consent_version_fk=self.consent_version_2,
                                                                 consent_date=datetime.date.today())
        self.consent_contract_1_cg_2 = ConsentContract.objects.create(caregiver_fk=self.second_caregiver,
                                                                      consent_version_fk=self.consent_version_1,
                                                                      consent_date=datetime.date.today())

        #create biospecimen

        self.completed = Outcome.objects.create(outcome=Outcome.OutcomeChoices.COMPLETED)
        self.incomplete = Outcome.objects.create(outcome=Outcome.OutcomeChoices.NOT_COLLECTED)
        # self.collected = Outcome.objects.create(status='Collected')

        self.processed_one = Processed.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                      processed_date_time=timezone.datetime(2023,5,5,12,4,0,tzinfo=pytz.UTC),
                                                      quantity =2,
                                                      logged_date_time=timezone.datetime(2023,5,5,12,4,0,tzinfo=pytz.UTC),
                                                      outcome_fk=self.completed)
        self.stored_one = Stored.objects.create(outcome_fk=self.completed,
                                                stored_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                storage_location='hospital',
                                                quantity=2,
                                                logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))

        self.shipped_one = Shipped.objects.create(outcome_fk=self.completed,
                                                  shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                  courier='Fedex',
                                                  shipping_number='7777777',
                                                  quantity=3,
                                                  logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))
        self.received_one = Received.objects.create(outcome_fk=self.completed,
                                                    received_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                    storage_location='MSU',
                                                    logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                    quantity=19)

        self.collected_one = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                      processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      received_date=timezone.datetime(2023,5,3).date(),
                                                      number_of_tubes=5,
                                                      in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
                                                      logged_by=self.test_user
                                                      )

        self.collected_two = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                      processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      received_date=timezone.datetime(2023,5,6).date(),
                                                      number_of_tubes=0,
                                                      in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
                                                      logged_by=self.test_user
                                                      )

        self.collected_three = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                      processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
                                                      received_date=timezone.datetime(2023,5,3).date(),
                                                      number_of_tubes=4,
                                                      in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
                                                      logged_by=self.test_user
                                                      )

        self.shipped_wsu_blank = ShippedWSU.objects.create(shipped_by=self.test_user)
        self.shipped_wsu = ShippedWSU.objects.create(shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
                                                     number_of_tubes=1,
                                                     courier='FedEx',
                                                     tracking_number='777777',
                                                     shipped_by=self.test_user
                                                     )

        self.shipped_echo_incomplete = ShippedECHO.objects.create()
        self.shipped_echo_complete = ShippedECHO.objects.create(shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))

        self.kit_sent = KitSent.objects.create(kit_sent_date=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))


        self.status_outcome_processed_complete_one = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_two = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_three = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_four = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_five = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_six = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_seven = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_eight = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_nine = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_ten = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_eleven = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_twelve = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_thirteen = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_fourteen = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_processed_complete_fifteen = Status.objects.create(processed_fk=self.processed_one)

        self.status_outcome_incomplete_one = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_two = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_three = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_four = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_five = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_six = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_seven = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_eight = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_nine = Status.objects.create(processed_fk=self.processed_one)
        self.status_outcome_incomplete_ten = Status.objects.create(processed_fk=self.processed_one)

        self.status_outcome_stored_complete = Status.objects.create(processed_fk=self.processed_one,stored_fk=self.stored_one)
        self.status_outcome_shipped_complete = Status.objects.create(processed_fk=self.processed_one,
                                                                     stored_fk=self.stored_one,shipped_fk=self.shipped_one)
        self.status_outcome_received_complete = Status.objects.create(processed_fk=self.processed_one,
                                                                      stored_fk=self.stored_one,
                                                                      shipped_fk=self.shipped_one,
                                                                      received_fk=self.received_one)



        self.status_outcome_collected_complete = Status.objects.create(collected_fk=self.collected_one)
        self.status_outcome_shipped_wsu_incomplete = Status.objects.create(collected_fk=self.collected_three,shipped_wsu_fk=self.shipped_wsu_blank)
        self.status_outcome_shipped_wsu_complete = Status.objects.create(collected_fk=self.collected_three,shipped_wsu_fk=self.shipped_wsu)
        self.status_outcome_shipped_echo_incomplete = Status.objects.create(collected_fk=self.collected_three,shipped_echo_fk=self.shipped_echo_incomplete)
        self.status_outcome_shipped_echo_complete = Status.objects.create(collected_fk=self.collected_three,shipped_echo_fk=self.shipped_echo_complete)

        self.status_outcome_collected_placenta = Status.objects.create(collected_fk=self.collected_two)
        self.status_outcome_blank = Status.objects.create()
        self.status_outcome_blank2  = Status.objects.create()

        self.status_kit_sent = Status.objects.create(kit_sent_fk=self.kit_sent)

        # self.status_outcome_collected = Status.objects.create(outcome_fk=self.incomplete,processed_fk=self.processed_one)

        self.urine = CollectionType.objects.create(collection_type='Urine')
        self.serum = CollectionType.objects.create(collection_type='Serum')
        self.plasma = CollectionType.objects.create(collection_type='Plasma')
        self.bloodspots = CollectionType.objects.create(collection_type='Bloodspots')
        self.whole_blood = CollectionType.objects.create(collection_type='Whole Blood')
        self.buffy_coat = CollectionType.objects.create(collection_type='Buffy Coat')
        self.red_blood_cells = CollectionType.objects.create(collection_type='Red Blood Cells')
        self.hair = CollectionType.objects.create(collection_type='Hair')
        self.toenail = CollectionType.objects.create(collection_type='Toenail')
        self.saliva = CollectionType.objects.create(collection_type='Saliva')
        self.placenta = CollectionType.objects.create(collection_type='Placenta')
        self.stool = CollectionType.objects.create(collection_type='Stool')
        self.tooth = CollectionType.objects.create(collection_type='Tooth')

        self.number_one = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.FIRST)
        self.number_two = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.SECOND)
        self.number_three = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.THIRD)
        self.number_early_childhood = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.EARLY_CHILDHOOD)
        self.number_middle_childhood= CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.MIDDLE_CHILDHOOD)


        self.urine_none = Collection.objects.create(collection_type_fk=self.urine)
        self.urine_one = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_one)
        self.urine_two = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_two)
        self.urine_three = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_three)
        self.urine_early_childhood = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_early_childhood)
        self.urine_mc = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_middle_childhood)

        self.serum_one = Collection.objects.create(collection_type_fk=self.serum, collection_number_fk=self.number_one)
        self.serum_two = Collection.objects.create(collection_type_fk=self.serum, collection_number_fk=self.number_two)
        self.serum_none = Collection.objects.create(collection_type_fk=self.serum)

        self.plasma_one = Collection.objects.create(collection_type_fk=self.plasma, collection_number_fk=self.number_one)
        self.plasma_two = Collection.objects.create(collection_type_fk=self.plasma, collection_number_fk=self.number_two)
        self.plasma_none = Collection.objects.create(collection_type_fk=self.plasma)

        self.bloodspots_one = Collection.objects.create(collection_type_fk=self.bloodspots, collection_number_fk=self.number_one)
        # self.bloodspots_two = Collection.objects.create(collection_type_fk='Bloodspots', collection_number_fk=self.number_two)

        self.whole_blood_one = Collection.objects.create(collection_type_fk=self.whole_blood, collection_number_fk=self.number_one)
        self.whole_blood_two = Collection.objects.create(collection_type_fk=self.whole_blood, collection_number_fk=self.number_two)
        self.whole_blood_none = Collection.objects.create(collection_type_fk=self.whole_blood)

        self.buffy_coat_one = Collection.objects.create(collection_type_fk=self.buffy_coat, collection_number_fk=self.number_one)
        self.buffy_coat_two = Collection.objects.create(collection_type_fk=self.buffy_coat, collection_number_fk=self.number_two)
        self.buffy_coat_none = Collection.objects.create(collection_type_fk=self.buffy_coat)

        self.red_blood_cells_one = Collection.objects.create(collection_type_fk=self.red_blood_cells, collection_number_fk=self.number_one)
        self.red_blood_cells_two = Collection.objects.create(collection_type_fk=self.red_blood_cells, collection_number_fk=self.number_two)
        self.red_blood_cells_none = Collection.objects.create(collection_type_fk=self.red_blood_cells)

        self.hair_early_childhood = Collection.objects.create(collection_type_fk=self.hair, collection_number_fk=self.number_early_childhood)
        self.hair_number_one = Collection.objects.create(collection_type_fk=self.hair,collection_number_fk=self.number_one)
        self.hair_none = Collection.objects.create(collection_type_fk=self.hair)

        self.toenail_earlychildhood = Collection.objects.create(collection_type_fk=self.toenail, collection_number_fk=self.number_early_childhood)
        self.toenail_one = Collection.objects.create(collection_type_fk=self.toenail,collection_number_fk=self.number_one)

        self.saliva_one = Collection.objects.create(collection_type_fk=self.saliva,collection_number_fk=self.number_one)

        self.stool_one = Collection.objects.create(collection_type_fk=self.stool,collection_number_fk=self.number_one)

        self.tooth_one = Collection.objects.create(collection_type_fk=self.tooth,collection_number_fk=self.number_one)
        self.tooth_two = Collection.objects.create(collection_type_fk=self.tooth,collection_number_fk=self.number_two)

        self.placenta_one = Collection.objects.create(collection_type_fk=self.placenta)
        self.placenta_two = Collection.objects.create(collection_type_fk=self.placenta, collection_number_fk=self.number_two)

        #Create perinatal event
        self.perinatal_one = Perinatal.objects.create(child_fk=self.child_one,pregnancy_fk=self.mother_one_pregnancy_one)


        #Create Biospeciment for Echo 2 Testing

        self.blood_trimester_1_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            trimester_fk=self.first_trimester,
            collection_fk=self.bloodspots_one,
            status_fk=self.status_outcome_blank2,
            biospecimen_id='1111BLS',
            project_fk=self.echo2
        )

        self.urine_trimester_1_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.first_caregiver,
            trimester_fk=self.first_trimester,
            collection_fk=self.urine_none,
            status_fk=self.status_outcome_collected_complete,
            biospecimen_id='111URS',
            project_fk=self.echo2,
            incentive_fk=self.incentive_two
        )

        self.urine_trimester_2_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.first_caregiver,
            trimester_fk=self.second_trimester,
            collection_fk=self.urine_none,
            biospecimen_id='112URS',
            project_fk=self.echo2
            #incentive_fk=self.incentive_two
        )

        self.urine_trimester_3_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.first_caregiver,
            trimester_fk=self.third_trimester,
            collection_fk=self.urine_none,
            status_fk=self.status_outcome_shipped_wsu_incomplete,
            biospecimen_id='113URS',
            project_fk=self.echo2,
            incentive_fk=self.incentive_two
        )

        self.urine_trimester_3_caregiver_two = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.second_caregiver,
            trimester_fk=self.first_trimester,
            collection_fk=self.urine_none,
            status_fk=self.status_outcome_shipped_wsu_complete,
            biospecimen_id='211URS',
            project_fk=self.echo2,
            incentive_fk=self.incentive_two
        )


        self.urine_trimester_2_caregiver_two = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.second_caregiver,
            trimester_fk=self.second_trimester,
            collection_fk=self.urine_none,
            status_fk=self.status_outcome_shipped_echo_incomplete,
            biospecimen_id='212URS',
            project_fk=self.echo2,
            incentive_fk=self.incentive_two
        )

        self.urine_trimester_3_caregiver_two = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.second_caregiver,
            trimester_fk=self.third_trimester,
            collection_fk=self.urine_none,
            status_fk=self.status_outcome_shipped_echo_complete,
            biospecimen_id='213URS',
            project_fk=self.echo2,
            incentive_fk=self.incentive_two
        )

        self.placenta_perinatal_2_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.first_caregiver,
            perinatal_fk=self.perinatal_one,
            collection_fk=self.placenta_one,
            status_fk=self.status_outcome_collected_placenta,
            biospecimen_id='111P1',
            project_fk=self.echo1,
            incentive_fk=self.incentive_two
        )

        self.new_status = Status.objects.create()

        self.whole_blood_caregiver_one_trimester_one = CaregiverBiospecimen.objects.create(
            caregiver_fk = self.first_caregiver,
            collection_fk=self.whole_blood_none,
            biospecimen_id='2111WB',
            project_fk=self.echo2,
            trimester_fk=self.first_trimester
        )



        #Create bloodspot rows for testing of application
        self.biospecimen_bloodspots_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_received_complete,
            collection_fk=self.bloodspots_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1111BS',
            project_fk=self.echo1)

        self.biospecimen_bloodspots_caregiver_three = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.third_caregiver,
            status_fk=self.status_outcome_processed_complete_one,
            collection_fk=self.bloodspots_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1114BS',
            project_fk=self.echo1)

        self.biospecimen_bloodspots_caregiver_four = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.fourth_caregiver,
            status_fk=self.status_outcome_stored_complete,
            collection_fk=self.bloodspots_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1115BS',
            project_fk=self.echo1)

        self.biospecimen_bloodspots_caregiver_five = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.fifth_caregiver,
            status_fk=self.status_outcome_shipped_complete,
            collection_fk=self.bloodspots_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1116BS',
            project_fk=self.echo1)

        self.biospecimen_urine_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_two,
            collection_fk=self.urine_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1111UR',
            project_fk=self.echo1)

        self.biospecimen_urine_one_caregiver_two = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.second_caregiver,
            status_fk=self.status_outcome_processed_complete_three,
            collection_fk=self.urine_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1112UR',
            project_fk=self.echo1)

        self.biospecimen_urine_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_one,
            collection_fk=self.urine_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1113UR',
            project_fk=self.echo1)

        self.biospecimen_urine_ec_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                      status_fk=self.status_outcome_incomplete_two,
                                                                                      collection_fk=self.urine_early_childhood,
                                                                                      incentive_fk=self.incentive_one,
                                                                                      biospecimen_date=datetime.date.today(),
                                                                                      biospecimen_id='1115UR',
            project_fk=self.echo1)

        self.biospecimen_urine_mc_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
                                                                                      status_fk=self.status_outcome_incomplete_three,
                                                                                      collection_fk=self.urine_mc,
                                                                                      incentive_fk=self.incentive_one,
                                                                                      biospecimen_date=datetime.date.today(),
                                                                                      biospecimen_id='1116UR',
            project_fk=self.echo1)

        self.biospecimen_serum_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_four,
            collection_fk=self.serum_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date(2023, 8, 23),
            biospecimen_id='1111SR',
            project_fk=self.echo1)

        self.biospecimen_serum_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_four,
            collection_fk=self.serum_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1112SR',
            project_fk=self.echo1)

        self.biospecimen_plasma_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_five,
            collection_fk=self.plasma_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1111PL',
            project_fk=self.echo1)

        self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_five,
            collection_fk=self.plasma_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1112PL',
            project_fk=self.echo1)



        # self.biospecimen_bloodspots_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete,
        #     collection_fk=self.bloodspots_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        # biospecimen_id='1112BS')

        self.biospecimen_whole_blood_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_six,
            collection_fk=self.whole_blood_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1111WB',
            project_fk=self.echo1)

        self.biospecimen_whole_blood_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_six,
            collection_fk=self.whole_blood_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1112WB',
            project_fk=self.echo1)

        self.biospecimen_buffy_coat_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_seven,
            collection_fk=self.buffy_coat_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),
            biospecimen_id='1111BC',
            project_fk=self.echo1)

        self.biospecimen_buffy_coat_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_seven,
            collection_fk=self.buffy_coat_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),biospecimen_id='1112BC',
            project_fk=self.echo1
        )

        self.biospecimen_red_blood_cells_one_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_eight,
            collection_fk=self.red_blood_cells_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),biospecimen_id='1111RB',
            project_fk=self.echo1)

        self.biospecimen_red_blood_cells_two_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_incomplete_eight,
            collection_fk=self.red_blood_cells_two,
            incentive_fk=self.incentive_one,
            biospecimen_date=datetime.date.today(),biospecimen_id='1112RB',
            project_fk=self.echo1)

        self.biospecimen_hair_early_childhood_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_nine,
            collection_fk=self.hair_early_childhood,
            incentive_fk=self.incentive_one,
            biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111HR',
            project_fk=self.echo1)

        self.biospecimen_toenail_prenatal_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_ten,
            collection_fk=self.toenail_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111TN',
            project_fk=self.echo1)

        self.biospecimen_salvia_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=self.status_outcome_processed_complete_eleven,
            collection_fk=self.saliva_one,
            incentive_fk=self.incentive_one,
            biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111SA',
            project_fk=self.echo1)


        self.biospecimen_hair_caregiver_one = CaregiverBiospecimen.objects.create(
            caregiver_fk=self.first_caregiver,
            status_fk=None,
            collection_fk=self.hair_none,
            incentive_fk=self.incentive_one,
            biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111HA',
            project_fk=self.echo2,
            age_category_fk=self.zero_to_five_age_category)


        #self.non_mother_one = NonPrimaryCaregiver.objects.create(caregiver_fk=self.second_caregiver,relation_fk=self.mother_in_law)


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


        #create child address

        # create child address

        self.child_address = ChildAddress.objects.create(child_fk=self.child_one, address_fk=self.address)

        #create child survey

        self.survey_that_child_takes = Survey.objects.create(survey_name='Eight Year Survey',project_fk=self.new_project)
        self.other_survey_that_child_takes = Survey.objects.create(survey_name='Five Year Survey',project_fk=self.new_project)

        self.child_one_survey_one = ChildSurvey.objects.create(child_fk=self.child_one,
                                                               survey_fk=self.survey_that_child_takes,
                                                               survey_outcome_fk=self.completed_survey_outcome,
                                                               survey_completion_date=timezone.datetime(2023,5,3).date())

        self.child_two_survey_one = ChildSurvey.objects.create(child_fk=self.child_two,
                                                               survey_fk=self.other_survey_that_child_takes,
                                                               survey_outcome_fk=self.incomplete_survey_outcome,
                                                               survey_completion_date=timezone.datetime(2023,5,4).date())



        #child assent
        self.eight_year_assent = Assent.objects.create(assent_text='Eight Year Survey')
        self.five_year_assent = Assent.objects.create(assent_text='Five Year Survey')
        self.child_one_eight_year_assent = ChildAssent.objects.create(child_fk=self.child_one,
                                                                      assent_fk=self.eight_year_assent,
                                                                      assent_date=timezone.datetime(2023,5,4).date(),assent_boolean=True)
        self.child_two_five_year_assent = ChildAssent.objects.create(child_fk=self.child_two,
                                                                     assent_fk=self.five_year_assent,
                                                                     assent_date=timezone.datetime(2023,5,4).date(),assent_boolean=False)

        # child biospecimen

        self.child_one_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                           status_fk=self.status_outcome_processed_complete_nine,
                                                                           collection_fk=self.urine_three,
                                                                           age_category_fk=self.early_childhood_age_category,
                                                                           collection_date=datetime.date(2023, 8, 15))

        self.child_two_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_two,
                                                                           status_fk=self.status_outcome_processed_complete_ten,
                                                                           collection_fk=self.urine_three,
                                                                           age_category_fk=self.early_childhood_age_category,
                                                                           collection_date=datetime.date(2023, 8, 15))

        self.child_one_biospecimen_hair = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                          status_fk=self.status_outcome_processed_complete_eleven,
                                                                          collection_fk=self.hair_number_one,
                                                                          age_category_fk=self.early_childhood_age_category,
                                                                          collection_date=datetime.date(2023, 8, 15))

        self.child_one_biospecimen_toenail = ChildBiospecimen.objects.create(child_fk=self.child_one,
                                                                             status_fk=self.status_outcome_processed_complete_twelve,
                                                                             collection_fk=self.toenail_one,
                                                                             age_category_fk=self.early_childhood_age_category,
                                                                             collection_date=datetime.date(2023, 8, 15))


        self.child_three_urine_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.urine_none,
                                                                             age_category_fk=self.zero_to_five_age_category,
                                                                             collection_date=datetime.date(2023, 8, 15)
                                                                             )

        self.child_three_stool_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.stool_one,
                                                                             age_category_fk=self.zero_to_five_age_category,
                                                                             collection_date=datetime.date(2023, 8, 10)
                                                                             )

        self.child_three_bloodspots_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.bloodspots_one,
                                                                             age_category_fk=self.zero_to_five_age_category,
                                                                             collection_date=datetime.date(2023, 8, 10)
                                                                             )

        self.child_three_bloodspots_12_to_13_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.bloodspots_one,
                                                                             age_category_fk=self.twelve_to_thirteen_months,
                                                                             collection_date=datetime.date(2023, 8, 10)
                                                                             )


        self.child_three_hair_12_to_13_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.hair_number_one,
                                                                             age_category_fk=self.twelve_to_thirteen_months,
                                                                             collection_date=datetime.date(2023, 8, 10)
                                                                             )


        self.child_three_teeth_six_ten_years = ChildBiospecimen.objects.create(child_fk=self.child_three,
                                                                             collection_fk=self.tooth_one,
                                                                             age_category_fk=self.six_to_ten_years,
                                                                             collection_date=datetime.date(2023, 8, 10)
                                                                             )



def tearDown(self):
            self.browser.quit()

