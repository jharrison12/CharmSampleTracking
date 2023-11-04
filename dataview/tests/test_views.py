import logging
import unittest
from django.test import TestCase
from dataview.models import Child, PrimaryCaregiver,ChildAddress
import datetime
from django.utils import timezone
from dataview.forms import CaregiverBiospecimenForm, IncentiveForm
from django.utils.html import escape
from dataview.tests.db_setup import DatabaseSetup

logging.basicConfig(level=logging.CRITICAL)

# Create your tests here.
class HomePageTest(DatabaseSetup):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dataview/home.html')


class CaregiverPageTest(DatabaseSetup):

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

class CaregiverInformationPageTest(DatabaseSetup):

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

    def test_caregiver_information_page_shows_pregnancy_for_pregnant_mom(self):
        response = self.client.get(f'/data/caregiver/P7000/')
        self.assertContains(response, 'Pregnancy Information:')

    def test_caregiver_information_page_does_not_show_pregnancy_info_for_non_mom(self):
        response = self.client.get(f'/data/caregiver/P7001/')
        self.assertNotContains(response, 'Pregnancy Information:')

class CaregiverSurveyPageTest(DatabaseSetup):

    def test_caregiver_survey_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertTemplateUsed(response, 'dataview/caregiver_survey.html')

    def test_caregiver_survey_page_shows_prenatal1_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 1: Complete')

    def test_caregiver_survey_page_shows_prenatal2_survey_outcome(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertContains(response,'Prenatal 2: Incomplete')

class CaregiverConsentItemPage(DatabaseSetup):

    def test_caregiver_consent_item_page_returns_correct_template(self):
        response = self.client.get(f'/data/caregiver/P7000/consentitem/')
        self.assertTemplateUsed(response,'dataview/caregiver_consent_item.html')

    def test_caregiver_consent_shows_mother_placenta(self):
        response = self.client.get(f'/data/caregiver/P7000/consentitem/')
        self.assertContains(response, "Mother Placenta")

class ChildPage(DatabaseSetup):

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

class ChildInformationPage(DatabaseSetup):

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
        response = self.client.get(f'/data/child/7003M1/')
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
        new_primary = PrimaryCaregiver.objects.create(caregiver_fk=self.first_caregiver)
        child_three = Child.objects.create(primary_care_giver_fk=new_primary,
                                           charm_project_identifier='7003M1',
                                           birth_hospital=self.health_care_facility_1,
                                           birth_sex=Child.BirthSexChoices.FEMALE,
                                           birth_date=datetime.date(2021, 8, 10),
                                           child_twin=False, pregnancy_fk=self.mother_one_pregnancy_one)
        new_child_address = ChildAddress.objects.create(address_fk=self.address, child_fk=child_three)

        response = self.client.get(f'/data/child/7003M1/')
        self.assertContains(response,'One Drive')

class ChildSurveyPage(DatabaseSetup):

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

class ChildAssentPage(DatabaseSetup):

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
        response = self.client.get(f'/data/child/7003M1/')
        self.assertEqual(response.status_code,404)

class CheckthatLoginRequired(DatabaseSetup):

    def setUp(self):
        self.client.logout()

    def test_logged_out_user_cant_see_home_page(self):
        response = self.client.get('/')
        self.assertTemplateNotUsed(response, 'dataview/home.html')

    def test_logged_out_user_cant_see_caregiver_page(self):
        response = self.client.get('/data/caregiver/')
        self.assertTemplateNotUsed(response, 'dataview/caregiver.html')

    def test_logged_out_user_cant_see_caregiver_information_page(self):
        response = self.client.get('/data/caregiver/P7000/')
        self.assertTemplateNotUsed(response,'dataview/caregiver_info.html')

    def test_logged_out_user_cant_see_caregiver_survey_page(self):
        response = self.client.get(f'/data/caregiver/P7000/survey/')
        self.assertTemplateNotUsed(response, 'dataview/caregiver_survey.html')

    def test_logged_out_user_cant_see_caregiver_consent_item_page(self):
        response = self.client.get(f'/data/caregiver/P7000/consentitem/')
        self.assertTemplateNotUsed(response,'dataview/caregiver_consent_item.html')

    def test_logged_out_user_cant_see_child_page(self):
        response = self.client.get(f'/data/child/')
        self.assertTemplateNotUsed(response,'dataview/child.html')

    def test_logged_out_user_cant_see_child_information_page(self):
        response = self.client.get(f'/data/child/7000M1/')
        self.assertTemplateNotUsed(response,'dataview/child_information.html')

    def test_logged_out_user_cant_see_child_survey_page(self):
        response = self.client.get(f'/data/child/7000M1/survey/')
        self.assertTemplateNotUsed(response,'dataview/child_survey.html')

    def test_logged_out_user_cant_see_child_assent_page(self):
        response = self.client.get(f'/data/child/7000M1/assent/')
        self.assertTemplateNotUsed(response,'dataview/child_assent.html')