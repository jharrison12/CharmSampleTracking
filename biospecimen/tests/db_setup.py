import logging
import sqlite3

from django.test import TestCase
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,\
    CollectionType,CollectionNumber,Collected,Trimester,Perinatal,ShippedWSU,ShippedECHO,AgeCategory,KitSent,User,Caregiver,Incentive,Project,\
    Child,Pregnancy
import datetime, pytz
from django.utils import timezone
from django.core.exceptions import ValidationError

logging.basicConfig(level=logging.CRITICAL)

class DatabaseSetup(TestCase):
    fixtures = ['initialdata']

    def setUp(self):
        self.client.login(username='testuser',password='secret')

        # ##Update Below
        #
        #
        # self.first_caregiver = Caregiver.objects.create(charm_project_identifier='P7000',
        #                                                 specimen_id='4444')
        #
        # self.second_caregiver = Caregiver.objects.create(charm_project_identifier='P7001',
        #                                                  specimen_id='5555')
        #
        # self.third_caregiver = Caregiver.objects.create(charm_project_identifier='P7002',
        #                                                 specimen_id='6666')
        #
        # self.fourth_caregiver = Caregiver.objects.create(charm_project_identifier='P7003',
        #                                                  specimen_id='7777')
        #
        # self.fifth_caregiver = Caregiver.objects.create(charm_project_identifier='P7004',
        #                                                 specimen_id='8888')
        #
        # #create incentive
        #
        # self.incentive_one = Incentive.objects.create(incentive_amount=100,incentive_type=Incentive.IncentiveType.GIFT_CARD)
        # self.incentive_two = Incentive.objects.create(incentive_type=Incentive.IncentiveType.GIFT_CARD,incentive_amount=100,incentive_date=timezone.datetime(2023, 8, 4).date())
        #
        # #create mother and nonmother caregiver tables
        #
        # self.mother_one_pregnancy_one = Pregnancy.objects.create(mother_fk=self.first_caregiver,
        #                                                          pregnancy_id=f"{self.first_caregiver.charm_project_identifier}F"
        #                                                          )
        #
        # # create trimester
        #
        # self.first_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.FIRST,pregnancy_fk=self.mother_one_pregnancy_one)
        # self.second_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.SECOND,pregnancy_fk=self.mother_one_pregnancy_one)
        # self.third_trimester = Trimester.objects.create(trimester=Trimester.TrimesterChoices.THIRD,pregnancy_fk=self.mother_one_pregnancy_one)
        #
        # self.early_childhood_age_category = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.EARLY_CHILDHOOD)
        # self.zero_to_five_age_category = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.ZERO_TO_FIVE)
        # self.twelve_to_thirteen_months = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.TWELVE_TO_THIRTEEN_MONTHS)
        # self.six_to_ten_years = AgeCategory.objects.create(age_category=AgeCategory.AgeCategoryChoice.SIX_TO_TEN_YEARS)
        #
        # #create primary care_giver
        #
        # # create child
        #
        # self.child_one = Child.objects.create(caregiver_fk=self.first_caregiver,
        #                                       charm_project_identifier='7000M1',
        #                                       pregnancy_fk=self.mother_one_pregnancy_one)
        # self.mother_one_pregnancy_one.save()
        # self.child_two = Child.objects.create(caregiver_fk=self.first_caregiver,
        #                                       charm_project_identifier='7001M1',
        #                                       pregnancy_fk=self.mother_one_pregnancy_one)
        #
        # self.child_three = Child.objects.create(caregiver_fk=self.first_caregiver,
        #                                       charm_project_identifier='7002M1',
        #                                       pregnancy_fk=self.mother_one_pregnancy_one)
        #
        # self.new_project = Project.objects.create(project_name='MARCH')
        # self.echo1 = Project.objects.create(project_name='ECHO1')
        # self.echo2 = Project.objects.create(project_name='ECHO2')
        #
        # #create biospecimen
        #
        # self.completed = Outcome.objects.create(outcome=Outcome.OutcomeChoices.COMPLETED)
        # self.incomplete = Outcome.objects.create(outcome=Outcome.OutcomeChoices.NOT_COLLECTED)
        # # self.collected = Outcome.objects.create(status='Collected')
        #
        # self.processed_one = Processed.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                               processed_date_time=timezone.datetime(2023,5,5,12,4,0,tzinfo=pytz.UTC),
        #                                               quantity =2,
        #                                               logged_date_time=timezone.datetime(2023,5,5,12,4,0,tzinfo=pytz.UTC),
        #                                               outcome_fk=self.completed)
        # self.stored_one = Stored.objects.create(outcome_fk=self.completed,
        #                                         stored_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                         storage_location='hospital',
        #                                         quantity=2,
        #                                         logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))
        #
        # self.shipped_one = Shipped.objects.create(outcome_fk=self.completed,
        #                                           shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                           courier='Fedex',
        #                                           shipping_number='7777777',
        #                                           quantity=3,
        #                                           logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))
        # self.received_one = Received.objects.create(outcome_fk=self.completed,
        #                                             received_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                             storage_location='MSU',
        #                                             logged_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                             quantity=19)
        #
        # self.collected_one = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                               processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               received_date=timezone.datetime(2023,5,3).date(),
        #                                               number_of_tubes=5,
        #                                               in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
        #                                               logged_by=self.test_user
        #                                               )
        #
        # self.collected_two = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                               processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               received_date=timezone.datetime(2023,5,6).date(),
        #                                               number_of_tubes=0,
        #                                               in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
        #                                               logged_by=self.test_user
        #                                               )
        #
        # self.collected_three = Collected.objects.create(collected_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                               processed_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               stored_date_time=timezone.datetime(2023,5,5,13,0,0,tzinfo=pytz.UTC),
        #                                               received_date=timezone.datetime(2023,5,3).date(),
        #                                               number_of_tubes=4,
        #                                               in_person_remote=Collected.InpersonRemoteChoices.IN_PERSON,
        #                                               logged_by=self.test_user
        #                                               )
        #
        # self.shipped_wsu_blank = ShippedWSU.objects.create(shipped_by=self.test_user)
        # self.shipped_wsu = ShippedWSU.objects.create(shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC),
        #                                              number_of_tubes=1,
        #                                              courier='FedEx',
        #                                              tracking_number='777777',
        #                                              shipped_by=self.test_user
        #                                              )
        #
        # self.shipped_echo_incomplete = ShippedECHO.objects.create()
        # self.shipped_echo_complete = ShippedECHO.objects.create(shipped_date_time=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))
        #
        # self.kit_sent = KitSent.objects.create(kit_sent_date=timezone.datetime(2023,5,5,12,0,0,tzinfo=pytz.UTC))
        #
        #
        # self.status_outcome_processed_complete_one = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_two = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_three = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_four = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_five = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_six = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_seven = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_eight = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_nine = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_ten = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_eleven = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_twelve = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_thirteen = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_fourteen = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_processed_complete_fifteen = Status.objects.create(processed_fk=self.processed_one)
        #
        # self.status_outcome_incomplete_one = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_two = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_three = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_four = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_five = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_six = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_seven = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_eight = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_nine = Status.objects.create(processed_fk=self.processed_one)
        # self.status_outcome_incomplete_ten = Status.objects.create(processed_fk=self.processed_one)
        #
        # self.status_outcome_stored_complete = Status.objects.create(processed_fk=self.processed_one,stored_fk=self.stored_one)
        # self.status_outcome_shipped_complete = Status.objects.create(processed_fk=self.processed_one,
        #                                                              stored_fk=self.stored_one,shipped_fk=self.shipped_one)
        # self.status_outcome_received_complete = Status.objects.create(processed_fk=self.processed_one,
        #                                                               stored_fk=self.stored_one,
        #                                                               shipped_fk=self.shipped_one,
        #                                                               received_fk=self.received_one)
        #
        #
        #
        # self.status_outcome_collected_complete = Status.objects.create(collected_fk=self.collected_one)
        # self.status_outcome_shipped_wsu_incomplete = Status.objects.create(collected_fk=self.collected_three,shipped_wsu_fk=self.shipped_wsu_blank)
        # self.status_outcome_shipped_wsu_complete = Status.objects.create(collected_fk=self.collected_three,shipped_wsu_fk=self.shipped_wsu)
        # self.status_outcome_shipped_echo_incomplete = Status.objects.create(collected_fk=self.collected_three,shipped_echo_fk=self.shipped_echo_incomplete)
        # self.status_outcome_shipped_echo_complete = Status.objects.create(collected_fk=self.collected_three,shipped_echo_fk=self.shipped_echo_complete)
        #
        # self.status_outcome_collected_placenta = Status.objects.create(collected_fk=self.collected_two)
        # self.status_outcome_blank = Status.objects.create()
        # self.status_outcome_blank2  = Status.objects.create()
        #
        # self.status_kit_sent = Status.objects.create(kit_sent_fk=self.kit_sent)
        #
        # # self.status_outcome_collected = Status.objects.create(outcome_fk=self.incomplete,processed_fk=self.processed_one)
        #
        # self.urine = CollectionType.objects.create(collection_type='Urine')
        # self.serum = CollectionType.objects.create(collection_type='Serum')
        # self.plasma = CollectionType.objects.create(collection_type='Plasma')
        # self.bloodspots = CollectionType.objects.create(collection_type='Bloodspots')
        # self.whole_blood = CollectionType.objects.create(collection_type='Whole Blood')
        # self.buffy_coat = CollectionType.objects.create(collection_type='Buffy Coat')
        # self.red_blood_cells = CollectionType.objects.create(collection_type='Red Blood Cells')
        # self.hair = CollectionType.objects.create(collection_type='Hair')
        # self.toenail = CollectionType.objects.create(collection_type='Toenail')
        # self.saliva = CollectionType.objects.create(collection_type='Saliva')
        # self.placenta = CollectionType.objects.create(collection_type='Placenta')
        # self.stool = CollectionType.objects.create(collection_type='Stool')
        # self.tooth = CollectionType.objects.create(collection_type='Tooth')
        #
        # self.number_one = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.FIRST)
        # self.number_two = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.SECOND)
        # self.number_three = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.THIRD)
        # self.number_early_childhood = CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.EARLY_CHILDHOOD)
        # self.number_middle_childhood= CollectionNumber.objects.create(collection_number=CollectionNumber.CollectionNumberChoices.MIDDLE_CHILDHOOD)
        #
        #
        # self.urine_none = Collection.objects.create(collection_type_fk=self.urine)
        # self.urine_one = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_one)
        # self.urine_two = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_two)
        # self.urine_three = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_three)
        # self.urine_early_childhood = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_early_childhood)
        # self.urine_mc = Collection.objects.create(collection_type_fk=self.urine, collection_number_fk=self.number_middle_childhood)
        #
        # self.serum_one = Collection.objects.create(collection_type_fk=self.serum, collection_number_fk=self.number_one)
        # self.serum_two = Collection.objects.create(collection_type_fk=self.serum, collection_number_fk=self.number_two)
        # self.serum_none = Collection.objects.create(collection_type_fk=self.serum)
        #
        # self.plasma_one = Collection.objects.create(collection_type_fk=self.plasma, collection_number_fk=self.number_one)
        # self.plasma_two = Collection.objects.create(collection_type_fk=self.plasma, collection_number_fk=self.number_two)
        # self.plasma_none = Collection.objects.create(collection_type_fk=self.plasma)
        #
        # self.bloodspots_one = Collection.objects.create(collection_type_fk=self.bloodspots, collection_number_fk=self.number_one)
        # # self.bloodspots_two = Collection.objects.create(collection_type_fk='Bloodspots', collection_number_fk=self.number_two)
        #
        # self.whole_blood_one = Collection.objects.create(collection_type_fk=self.whole_blood, collection_number_fk=self.number_one)
        # self.whole_blood_two = Collection.objects.create(collection_type_fk=self.whole_blood, collection_number_fk=self.number_two)
        # self.whole_blood_none = Collection.objects.create(collection_type_fk=self.whole_blood)
        #
        # self.buffy_coat_one = Collection.objects.create(collection_type_fk=self.buffy_coat, collection_number_fk=self.number_one)
        # self.buffy_coat_two = Collection.objects.create(collection_type_fk=self.buffy_coat, collection_number_fk=self.number_two)
        # self.buffy_coat_none = Collection.objects.create(collection_type_fk=self.buffy_coat)
        #
        # self.red_blood_cells_one = Collection.objects.create(collection_type_fk=self.red_blood_cells, collection_number_fk=self.number_one)
        # self.red_blood_cells_two = Collection.objects.create(collection_type_fk=self.red_blood_cells, collection_number_fk=self.number_two)
        # self.red_blood_cells_none = Collection.objects.create(collection_type_fk=self.red_blood_cells)
        #
        # self.hair_early_childhood = Collection.objects.create(collection_type_fk=self.hair, collection_number_fk=self.number_early_childhood)
        # self.hair_number_one = Collection.objects.create(collection_type_fk=self.hair,collection_number_fk=self.number_one)
        # self.hair_none = Collection.objects.create(collection_type_fk=self.hair)
        #
        # self.toenail_earlychildhood = Collection.objects.create(collection_type_fk=self.toenail, collection_number_fk=self.number_early_childhood)
        # self.toenail_one = Collection.objects.create(collection_type_fk=self.toenail,collection_number_fk=self.number_one)
        #
        # self.saliva_one = Collection.objects.create(collection_type_fk=self.saliva,collection_number_fk=self.number_one)
        # self.saliva_none = Collection.objects.create(collection_type_fk=self.saliva)
        #
        # self.stool_one = Collection.objects.create(collection_type_fk=self.stool,collection_number_fk=self.number_one)
        #
        # self.tooth_one = Collection.objects.create(collection_type_fk=self.tooth,collection_number_fk=self.number_one)
        # self.tooth_two = Collection.objects.create(collection_type_fk=self.tooth,collection_number_fk=self.number_two)
        #
        # self.placenta_one = Collection.objects.create(collection_type_fk=self.placenta)
        # self.placenta_two = Collection.objects.create(collection_type_fk=self.placenta, collection_number_fk=self.number_two)
        #
        # #Create perinatal event
        # self.perinatal_one = Perinatal.objects.create(child_fk=self.child_one,pregnancy_fk=self.mother_one_pregnancy_one)
        #
        #
        # #Create Biospeciment for Echo 2 Testing
        #
        # self.blood_trimester_1_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     trimester_fk=self.first_trimester,
        #     collection_fk=self.bloodspots_one,
        #     status_fk=self.status_outcome_blank2,
        #     biospecimen_id='1111BLS',
        #     project_fk=self.echo2
        # )
        #
        # self.urine_trimester_1_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     trimester_fk=self.first_trimester,
        #     collection_fk=self.urine_none,
        #     status_fk=self.status_outcome_collected_complete,
        #     biospecimen_id='111URS',
        #     project_fk=self.echo2,
        #     incentive_fk=self.incentive_two
        # )
        #
        # self.urine_trimester_2_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     trimester_fk=self.second_trimester,
        #     collection_fk=self.urine_none,
        #     biospecimen_id='112URS',
        #     project_fk=self.echo2
        #     #incentive_fk=self.incentive_two
        # )
        #
        # self.urine_trimester_3_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     trimester_fk=self.third_trimester,
        #     collection_fk=self.urine_none,
        #     status_fk=self.status_outcome_shipped_wsu_incomplete,
        #     biospecimen_id='113URS',
        #     project_fk=self.echo2,
        #     incentive_fk=self.incentive_two
        # )
        #
        # self.urine_trimester_3_caregiver_two = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.second_caregiver,
        #     trimester_fk=self.first_trimester,
        #     collection_fk=self.urine_none,
        #     status_fk=self.status_outcome_shipped_wsu_complete,
        #     biospecimen_id='211URS',
        #     project_fk=self.echo2,
        #     incentive_fk=self.incentive_two
        # )
        #
        #
        # self.urine_trimester_2_caregiver_two = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.second_caregiver,
        #     trimester_fk=self.second_trimester,
        #     collection_fk=self.urine_none,
        #     status_fk=self.status_outcome_shipped_echo_incomplete,
        #     biospecimen_id='212URS',
        #     project_fk=self.echo2,
        #     incentive_fk=self.incentive_two
        # )
        #
        # self.urine_trimester_3_caregiver_two = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.second_caregiver,
        #     trimester_fk=self.third_trimester,
        #     collection_fk=self.urine_none,
        #     status_fk=self.status_outcome_shipped_echo_complete,
        #     biospecimen_id='213URS',
        #     project_fk=self.echo2,
        #     incentive_fk=self.incentive_two
        # )
        #
        # self.placenta_perinatal_2_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     perinatal_fk=self.perinatal_one,
        #     collection_fk=self.placenta_one,
        #     status_fk=self.status_outcome_collected_placenta,
        #     biospecimen_id='111P2',
        #     project_fk=self.echo1,
        #     incentive_fk=self.incentive_two
        # )
        #
        # self.placenta_perinatal_1_caregiver_one_echo2 = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     perinatal_fk=self.perinatal_one,
        #     collection_fk=self.placenta_one,
        #     status_fk=None,
        #     biospecimen_id='111P1',
        #     project_fk=self.echo2
        # )
        #
        # self.new_status = Status.objects.create()
        #
        # self.whole_blood_caregiver_one_trimester_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk = self.first_caregiver,
        #     collection_fk=self.whole_blood_none,
        #     biospecimen_id='2111WB',
        #     project_fk=self.echo2,
        #     trimester_fk=self.first_trimester
        # )
        #
        #
        #
        # #Create bloodspot rows for testing of application
        # self.biospecimen_bloodspots_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_received_complete,
        #     collection_fk=self.bloodspots_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1111BS',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_bloodspots_caregiver_three = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.third_caregiver,
        #     status_fk=self.status_outcome_processed_complete_one,
        #     collection_fk=self.bloodspots_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1114BS',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_bloodspots_caregiver_four = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.fourth_caregiver,
        #     status_fk=self.status_outcome_stored_complete,
        #     collection_fk=self.bloodspots_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1115BS',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_bloodspots_caregiver_five = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.fifth_caregiver,
        #     status_fk=self.status_outcome_shipped_complete,
        #     collection_fk=self.bloodspots_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1116BS',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_urine_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_two,
        #     collection_fk=self.urine_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1111UR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_urine_one_caregiver_two = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.second_caregiver,
        #     status_fk=self.status_outcome_processed_complete_three,
        #     collection_fk=self.urine_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1112UR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_urine_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_one,
        #     collection_fk=self.urine_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1113UR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_urine_ec_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
        #                                                                               status_fk=self.status_outcome_incomplete_two,
        #                                                                               collection_fk=self.urine_early_childhood,
        #                                                                               incentive_fk=self.incentive_one,
        #                                                                               biospecimen_date=datetime.date.today(),
        #                                                                               biospecimen_id='1115UR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_urine_mc_caregiver_one = CaregiverBiospecimen.objects.create(caregiver_fk=self.first_caregiver,
        #                                                                               status_fk=self.status_outcome_incomplete_three,
        #                                                                               collection_fk=self.urine_mc,
        #                                                                               incentive_fk=self.incentive_one,
        #                                                                               biospecimen_date=datetime.date.today(),
        #                                                                               biospecimen_id='1116UR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_serum_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_four,
        #     collection_fk=self.serum_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date(2023, 8, 23),
        #     biospecimen_id='1111SR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_serum_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_four,
        #     collection_fk=self.serum_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1112SR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_plasma_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_five,
        #     collection_fk=self.plasma_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1111PL',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_plasma_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_five,
        #     collection_fk=self.plasma_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1112PL',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_whole_blood_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_six,
        #     collection_fk=self.whole_blood_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1111WB',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_whole_blood_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_six,
        #     collection_fk=self.whole_blood_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1112WB',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_buffy_coat_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_seven,
        #     collection_fk=self.buffy_coat_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),
        #     biospecimen_id='1111BC',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_buffy_coat_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_seven,
        #     collection_fk=self.buffy_coat_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),biospecimen_id='1112BC',
        #     project_fk=self.echo1
        # )
        #
        # self.biospecimen_red_blood_cells_one_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_eight,
        #     collection_fk=self.red_blood_cells_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),biospecimen_id='1111RB',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_red_blood_cells_two_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_incomplete_eight,
        #     collection_fk=self.red_blood_cells_two,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=datetime.date.today(),biospecimen_id='1112RB',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_hair_early_childhood_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_nine,
        #     collection_fk=self.hair_early_childhood,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111HR',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_toenail_prenatal_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_ten,
        #     collection_fk=self.toenail_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111TN',
        #     project_fk=self.echo1)
        #
        # self.biospecimen_salvia_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=self.status_outcome_processed_complete_eleven,
        #     collection_fk=self.saliva_one,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111SA',
        #     project_fk=self.echo1)
        #
        #
        # self.biospecimen_hair_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=None,
        #     collection_fk=self.hair_none,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111HA',
        #     project_fk=self.echo2,
        #     age_category_fk=self.zero_to_five_age_category)
        #
        # self.biospecimen_saliva_caregiver_one = CaregiverBiospecimen.objects.create(
        #     caregiver_fk=self.first_caregiver,
        #     status_fk=None,
        #     collection_fk=self.saliva_none,
        #     incentive_fk=self.incentive_one,
        #     biospecimen_date=timezone.datetime(2023,5,3).date(),biospecimen_id='1111SL',
        #     project_fk=self.echo2,
        #     age_category_fk=self.zero_to_five_age_category)
        #
        #
        # # child biospecimen
        #
        # self.child_one_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_one,
        #                                                                    status_fk=self.status_outcome_processed_complete_nine,
        #                                                                    collection_fk=self.urine_three,
        #                                                                    age_category_fk=self.early_childhood_age_category,
        #                                                                    collection_date=datetime.date(2023, 8, 15))
        #
        # self.child_two_biospecimen_urine = ChildBiospecimen.objects.create(child_fk=self.child_two,
        #                                                                    status_fk=self.status_outcome_processed_complete_ten,
        #                                                                    collection_fk=self.urine_three,
        #                                                                    age_category_fk=self.early_childhood_age_category,
        #                                                                    collection_date=datetime.date(2023, 8, 15))
        #
        # self.child_one_biospecimen_hair = ChildBiospecimen.objects.create(child_fk=self.child_one,
        #                                                                   status_fk=self.status_outcome_processed_complete_eleven,
        #                                                                   collection_fk=self.hair_number_one,
        #                                                                   age_category_fk=self.early_childhood_age_category,
        #                                                                   collection_date=datetime.date(2023, 8, 15))
        #
        # self.child_one_biospecimen_toenail = ChildBiospecimen.objects.create(child_fk=self.child_one,
        #                                                                      status_fk=self.status_outcome_processed_complete_twelve,
        #                                                                      collection_fk=self.toenail_one,
        #                                                                      age_category_fk=self.early_childhood_age_category,
        #                                                                      collection_date=datetime.date(2023, 8, 15))
        #
        #
        # self.child_three_urine_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.urine_none,
        #                                                                      age_category_fk=self.zero_to_five_age_category,
        #                                                                      collection_date=datetime.date(2023, 8, 15)
        #                                                                      )
        #
        # self.child_three_stool_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.stool_one,
        #                                                                      age_category_fk=self.zero_to_five_age_category,
        #                                                                      collection_date=datetime.date(2023, 8, 10)
        #                                                                      )
        #
        # self.child_three_bloodspots_zero_to_five_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.bloodspots_one,
        #                                                                      age_category_fk=self.zero_to_five_age_category,
        #                                                                      collection_date=datetime.date(2023, 8, 10)
        #                                                                      )
        #
        # self.child_three_bloodspots_12_to_13_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.bloodspots_one,
        #                                                                      age_category_fk=self.twelve_to_thirteen_months,
        #                                                                      collection_date=datetime.date(2023, 8, 10)
        #                                                                      )
        #
        #
        # self.child_three_hair_12_to_13_months = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.hair_number_one,
        #                                                                      age_category_fk=self.twelve_to_thirteen_months,
        #                                                                      collection_date=datetime.date(2023, 8, 10)
        #                                                                      )
        #
        #
        # self.child_three_teeth_six_ten_years = ChildBiospecimen.objects.create(child_fk=self.child_three,
        #                                                                      collection_fk=self.tooth_one,
        #                                                                      age_category_fk=self.six_to_ten_years,
        #                                                                      collection_date=datetime.date(2023, 8, 10)
        #                                                                      )
        #
        #
