import datetime
from django.utils import timezone
from django.db import models
import pytz
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
import logging
from django.contrib.auth.models import AbstractUser
logging.basicConfig(level=logging.CRITICAL)


class User(AbstractUser):
    pass


class Race(models.Model):
    class RaceChoice(models.TextChoices):
        AMERICAN_INDIAN = 'I',_('American Indian or Alaska Native')
        ASIAN = 'A', _('Asian')
        BLACK = 'B', _('Black or African American')
        PACIFIC_ISLANDER = 'P', _('Native Hawaiian or Other Pacific Islander')
        WHITE = 'W', _('White')
        UNKNOWN = 'U', _('Unknown')
    race = models.CharField(default=RaceChoice.UNKNOWN,choices=RaceChoice.choices, max_length=1)

class Ethnicity(models.Model):
    class EthnicityChoice(models.TextChoices):
        HISPANIC = 'H',_('Hispanic')
        NON_HISPANIC = 'N', _('Non-Hispanic')
        UNKNOWN = 'U',_('Unknown')
    ethnicity = models.CharField(default=EthnicityChoice.UNKNOWN,choices=EthnicityChoice.choices,max_length=1)

# Create your models here.
class Caregiver(models.Model):
    #caregiver_pk = models.AutoField(primary_key=True)
    #should race and ethnicity be nullable?
    race_fk = models.ForeignKey(Race,on_delete=models.PROTECT)
    ethnicity_fk = models.ForeignKey(Ethnicity, on_delete=models.PROTECT)
    charm_project_identifier = models.CharField(default='', max_length=6,unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    ewcp_participant_identifier = models.CharField(default='',max_length=16)
    participation_level_identifier = models.CharField(default='',max_length=2)
    echo_pin = models.CharField(default='',max_length=3)
    specimen_id = models.CharField(null=False,max_length=4,unique=True)

    def __str__(self):
        return self.charm_project_identifier

class Name(models.Model):
    #name_pk = models.AutoField(primary_key=True)
    first_name =models.CharField(max_length=255,null=False)
    last_name =models.CharField(max_length=255,null=False)
    middle_name =models.CharField(max_length=255)
    nick_name =models.CharField(max_length=255)
    maiden_name =models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CaregiverName(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    name_fk = models.ForeignKey(Name,on_delete=models.PROTECT)
    revision_number = models.IntegerField(default=1,null=False)
    class CaregiverNameStatusChoice (models.TextChoices):
        CURRENT = 'C', _('Current')
        ARCHIVED = 'A', _('Archived')
    status = models.CharField(default=CaregiverNameStatusChoice.CURRENT,choices=CaregiverNameStatusChoice.choices,max_length=1)
    eff_start_date = models.DateTimeField()
    eff_end_date = models.DateTimeField(default=datetime.datetime(2999, 12, 31, 0, 0, 0, 127325, tzinfo=pytz.UTC))

    def __str__(self):
        return f"{self.name_fk}"

    def return_most_recent_name(self):
        if self.status=='C':
            return self.name_fk.last_name, self.name_fk.first_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name_fk','status','caregiver_fk'], name=f"caregiver_name_unique_constraint")
        ]


class Address(models.Model):
    address_line_1 = models.CharField(default='', max_length=255)
    address_line_2 = models.CharField(default='', max_length=255)
    city = models.CharField(default='', max_length=255)
    state = models.CharField(default='MI', max_length=2)
    zip_code = models.CharField(default='',max_length=9)

    def __str__(self):
        return f"{self.address_line_1} {self.address_line_2 or ''} {self.city} {self.state}, {self.zip_code}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address_line_1','address_line_2','city','state','zip_code'],name=f"address_unique_constraint")
        ]

class CaregiverAddress(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)
    revision_number = models.IntegerField(null=False,default=1)
    class CaregiverAddressStatusChoice(models.TextChoices):
        CURRENT = 'C', _('Current')
        ARCHIVED = 'A', _('Archived')
        FUTURE = 'F', _('Future')
    status = models.CharField(default=CaregiverAddressStatusChoice.CURRENT,choices=CaregiverAddressStatusChoice.choices,max_length=1)
    eff_start_date = models.DateTimeField(default=datetime.datetime.today())
    eff_end_date = models.DateTimeField(default=datetime.datetime(2999, 12, 31, 0, 0, 0, 127325, tzinfo=pytz.UTC))

    def __str__(self):
        return f"{self.address_fk}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','address_fk'],name="caregiver_address_constraint")
        ]


class Email(models.Model):
    email = models.EmailField(null=True,unique=True)

    def __str__(self):
        return f"{self.email}"

class CaregiverEmail(models.Model):
    #Should make the combination of caregiver and email type unique?  Dont need more than one primary, etc.
    email_fk = models.ForeignKey(Email,on_delete=models.PROTECT)
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)

    class EmailTypeChoices(models.TextChoices):
        PRIMARY = 'PR',_('Primary')
        SECONDARY = 'SD',_('Secondary')
        INACTIVE = 'IN',_('Inactive')

    email_type = models.CharField(max_length=2,choices=EmailTypeChoices.choices,default=EmailTypeChoices.PRIMARY)

    date_change = models.DateField(blank=False,null=False,default=timezone.now)

    def __str__(self):
        return f"{self.email_fk}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email_fk','caregiver_fk','email_type'],
                                    name="caregiver_email_unique_constraint")
        ]

class Phone(models.Model):
    area_code = models.CharField(null=False,blank=False,max_length=3)
    phone_number = models.CharField(null=False,blank=False,max_length=8)

    def __str__(self):
        return f"{self.area_code}-{self.phone_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['area_code', 'phone_number'],
                                    name="phone_unique_constraint")
        ]

class CaregiverPhone(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    phone_fk = models.ForeignKey(Phone,on_delete=models.PROTECT)

    class CaregiverPhoneTypeChoices(models.TextChoices):
        PRIMARY = 'PR',_('Primary')
        SECONDARY = 'SD',_('Secondary')
        INACTIVE = 'IN',_('Inactive')

    phone_type = models.CharField(max_length=2,choices=CaregiverPhoneTypeChoices.choices,default=CaregiverPhoneTypeChoices.PRIMARY)
    date_change = models.DateField(blank=False,null=False,default=timezone.now)

    def __str__(self):
        return f"{self.phone_fk}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk', 'phone_fk','phone_type'],
                                    name="caregiver_phone_unique_constraint")
        ]

class SocialMedia(models.Model):
    social_media_name = models.CharField(null=True,blank=True,max_length=255,unique=True)

    def __str__(self):
        return f"{self.social_media_name}"

class CaregiverSocialMedia(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    social_media_fk = models.ForeignKey(SocialMedia,on_delete=models.PROTECT)
    social_media_user_name = models.CharField(null=False,blank=False,max_length=255)
    social_media_consent = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.social_media_user_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk', 'social_media_fk','social_media_user_name'],
                                    name="caregiver_social_media_unique_constraint")
        ]

class CaregiverSocialMediaHistory(models.Model):
    caregiver_social_media_fk = models.ForeignKey(CaregiverSocialMedia,on_delete=models.PROTECT)
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    social_media_fk = models.ForeignKey(SocialMedia,on_delete=models.PROTECT)
    social_media_user_name = models.CharField(null=False,blank=False,max_length=255)
    social_media_consent = models.BooleanField(default=True)
    revision_number = models.IntegerField(null=False)
    revision_date = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_social_media_fk', 'caregiver_fk','social_media_fk','social_media_user_name','revision_number'],
                                    name="caregiver_social_media_history_unique_constraint")
        ]

class CaregiverPersonalContact(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address, on_delete=models.PROTECT)
    name_fk = models.ForeignKey(Name,on_delete=models.PROTECT)
    phone_fk = models.ForeignKey(Phone,on_delete=models.PROTECT)
    email_fk = models.ForeignKey(Email,on_delete=models.PROTECT)

    class CaregiverPersonalContactTypeChoices(models.TextChoices):
        PRIMARY = 'PR',_('Primary')
        SECONDARY = 'SD',_('Secondary')
        INACTIVE = 'IN',_('Inactive')

    caregiver_contact_type = models.CharField(max_length=2,
                                              choices=CaregiverPersonalContactTypeChoices.choices,
                                              default=CaregiverPersonalContactTypeChoices.PRIMARY)

    date_change = models.DateField(blank=False,null=False,default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','name_fk'],
                                    name="caregiver_personal_contact_unique_constraint")
        ]

class IncentiveType(models.Model):
    incentive_type_text = models.CharField(null=False,blank=False,max_length=255,unique=True)

    def __str__(self):
        return self.incentive_type_text

class Incentive(models.Model):
    incentive_type_fk = models.ForeignKey(IncentiveType,on_delete=models.PROTECT)
    incentive_date = models.DateField(blank=False,null=False,default=timezone.now)
    incentive_amount =models.IntegerField(null=True)

    def __str__(self):
        return f"{self.incentive_type_fk}: {self.incentive_amount}"

class Project(models.Model):
    project_name = models.CharField(null=False, blank=False, max_length=255,unique=True)

    def __str__(self):
        return f"{self.project_name}"

class Survey(models.Model):
    project_fk = models.ForeignKey(Project, on_delete=models.PROTECT)
    survey_name = models.CharField(null=False, blank=False, max_length=255,unique=True)

    def __str__(self):
        return f"{self.survey_name}"

class SurveyOutcome(models.Model):
    survey_outcome_text = models.CharField(null=False, blank=False, max_length=255,unique=True)

    def __str__(self):
        return f"{self.survey_outcome_text}"

class CaregiverSurvey(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    survey_fk = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_outcome_fk = models.ForeignKey(SurveyOutcome, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive,on_delete=models.PROTECT,blank=True,null=True)
    survey_completion_date = models.DateField(blank=False, null=False, default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','survey_fk'],name="caregiver_survey_unique_constraint")
        ]

class HealthcareFacility(models.Model):
    name = models.CharField(null=False,blank=False,max_length=255,unique=True)

    def __str__(self):
        return f"{self.name}"

class Recruitment(models.Model):
    caregiver_fk = models.OneToOneField(Caregiver,on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive,on_delete=models.PROTECT)
    healthcare_facility_fk = models.ForeignKey(HealthcareFacility,on_delete=models.PROTECT)
    recruitment_date = models.DateField(blank=False,null=False,default=timezone.now)
    interviewer_comment = models.TextField(blank=True,null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','healthcare_facility_fk'],name="recruitment_unique_constraint")
        ]

class ConsentVersion(models.Model):
    consent_version = models.CharField(blank=False,null=False,max_length=255, unique=True)
    consent_version_text = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.consent_version}"

class ConsentContract(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    consent_version_fk = models.ForeignKey(ConsentVersion,on_delete=models.PROTECT)
    consent_date = models.DateField(default=timezone.now)
    #This needs to autoincrement but that is not easy in django, maybe remove?
    #I'm removing consent number because it can be calculated using date if they need it
    #consent_number = models.IntegerField()
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','consent_version_fk'],name="consent_contract_unique_constraint")
        ]

class Mother(models.Model):
    caregiver_fk = models.OneToOneField(Caregiver,on_delete=models.PROTECT,unique=True)

class Pregnancy(models.Model):
    mother_fk = models.ForeignKey(Mother,on_delete=models.PROTECT)
    pregnancy_id = models.CharField(max_length=255,unique=True)
    due_date = models.DateField(null=True,blank=True)
    last_menstrual_period = models.DateField(null=True,blank=True)
    gestational_age_at_birth = models.CharField(max_length=255)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['mother_fk','pregnancy_id'],name="pregnancy_unique_constraint")
        ]

    def __string__(self):
        return f"{self.pregnancy_id}"

    def calculate_gestational_age(self, today_or_dob=datetime.date.today()):
        gestational_age = today_or_dob - self.last_menstrual_period
        return f"{gestational_age.days//7}"

    # def clean(self):
    #     self.gestational_age = self.calculate_gestational_age()

    def save(self,*args,**kwargs):
        children = Child.objects.filter(pregnancy_fk__pregnancy_id=self.pregnancy_id)
        #need to use filter for twins.  This ONLY works if twins have the same dob.
        for child in children:
            if child.birth_date:
                self.gestational_age_at_birth = self.calculate_gestational_age(child.birth_date)
                break
            else:
                pass
        super().save(*args,**kwargs)

class Relation(models.Model):
    relation_type = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.relation_type

class NonPrimaryCaregiver(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    child_fk = models.ForeignKey("Child",on_delete=models.PROTECT)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['child_fk','caregiver_fk'],name="non_primary_caregiver_fk")
        ]

class PrimaryCaregiver(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.caregiver_fk.charm_project_identifier} PCG"




class ConsentType(models.Model):

    class ConsentTypeChoices(models.TextChoices):
        MOTHER_URINE = 'MTHR_UR',_('Mother Urine')
        MOTHER_BLOOD = 'MTHR_BLD',_('Mother Blood')
        MOTHER_PLACENTA = 'MTHR_PLCNT',_('Mother Placenta')
        NAIL_HAIR_URINE = 'MTHR_NL_HR_UR',_('Mother Nail Hair Urine')
        BIRTH_CERTIFICATE = 'BIRTH_CERT', _('Birth Certificate')
        MDHHS = 'MDHHS', _('Michigan Department of Health and Human Services')
        CHILD_POOP = 'CHLD_POOP', _('Child Poop')
        CHILD_TEETH = 'CHLD_TEETH', _('Child Teeth')
        SRV_HOME = 'SRV_HOME', _('Serve Home')
        ADDRESSB = 'ADDRS_B', _('Address B')
        CHILD_BLOOD = 'CHILD_BLD', _('Child Blood')
        INFO_SHARE = 'INFO_SHARE', _('Information Sharing')
        ADDRESS = 'ADDRESS', _('Address')
        DNA = 'DNA', _('DNA')
        OTHER_STUDY = 'OTH_STUDY', _('Other Study')
        UOFM = 'UOFM', _('University of Michigan')
        SOCIAL_MEDIA = 'SCL_MEDIA', _('Social Media')

    consent_type_text = models.CharField(max_length=20,
                                              choices=ConsentTypeChoices.choices)

    def __str__(self):
        return f"{self.consent_type_text}"


class ConsentItem(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    consent_type_fk = models.ForeignKey(ConsentType, on_delete=models.PROTECT)
    consent_boolean = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.consent_type_fk}: {self.consent_boolean}"

class Child(models.Model):
    primary_care_giver_fk = models.OneToOneField(PrimaryCaregiver, on_delete=models.PROTECT)
    pregnancy_fk = models.ForeignKey(Pregnancy,on_delete=models.PROTECT)
    race_fk = models.ForeignKey(Race,on_delete=models.PROTECT, null=True)
    ethnicity_fk = models.ForeignKey(Ethnicity, on_delete=models.PROTECT,null=True)
    charm_project_identifier = models.CharField(max_length=8, unique=True)
    birth_date = models.DateField(null=True)

    class BirthSexChoices(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    birth_sex = models.CharField(max_length=1, choices=BirthSexChoices.choices)
    birth_hospital = models.ForeignKey(HealthcareFacility,on_delete=models.PROTECT)
    child_interviewer_comments = models.TextField()
    child_twin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.charm_project_identifier}"

    def is_caregiver_mother(self):
        #pcg = PrimaryCaregiver.objects.get(child__charm_project_identifier=self.charm_project_identifier)
        if Mother.objects.filter(caregiver_fk__primarycaregiver=self.primary_care_giver_fk).exists():
            return True
        elif not Mother.objects.filter(caregiver_fk__primarycaregiver=self.primary_care_giver_fk).exists():
            return False
        else:
            raise Exception

    #todo calculate inactive status with function

class ChildName(models.Model):
    child_fk = models.ForeignKey(Child,on_delete=models.PROTECT)
    name_fk = models.ForeignKey(Name,on_delete=models.PROTECT)
    revision_number = models.IntegerField(default=0)
    class ChildNameStatusChoice (models.TextChoices):
        CURRENT = 'C', _('Current')
        ARCHIVED = 'A', _('Archived')

    status = models.CharField(max_length=1,choices=ChildNameStatusChoice.choices)
    effective_start_date = models.DateField(default=timezone.now)
    effective_end_date = models.DateField(default=datetime.date(2099,12,31))

    def __str__(self):
        return f"{self.name_fk.first_name} {self.name_fk.last_name}"

class ChildAddress(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["child_fk","address_fk"],name="child address unique constraint")
        ]

    def __str__(self):
        return f"{self.address_fk.address_line_1} {self.address_fk.address_line_2} {self.address_fk.city}, {self.address_fk.state} {self.address_fk.zip_code}"

class ChildAddressHistory(models.Model):
    child_address_fk = models.ForeignKey(ChildAddress, on_delete=models.PROTECT)
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)
    revision_number = models.IntegerField(default=0)
    revision_date = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child_address_fk','child_fk','address_fk','revision_number'],
                                    name="child_address_history_unique_constraint")
        ]

class ChildSurvey(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    survey_fk = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_outcome_fk = models.ForeignKey(SurveyOutcome,on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive,on_delete=models.PROTECT,null=True,blank=True)
    survey_completion_date = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child_fk','survey_fk'], name='child survey unique constraint')

        ]

    def __str__(self):
        return f"{self.child_fk.charm_project_identifier} {self.survey_fk.survey_name}"

class Assent(models.Model):
    assent_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.assent_text}"

class ChildAssent(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    assent_fk = models.ForeignKey(Assent, on_delete=models.PROTECT)
    assent_date = models.DateField(default=timezone.now)
    assent_boolean = models.BooleanField(default=True, null=False,blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child_fk','assent_fk'], name='child assent unique constraint')

        ]

    def __str__(self):
        return f"{self.child_fk.charm_project_identifier} {self.assent_fk.assent_text}"

class ChildAssentHistory(models.Model):
    child_assent_fk = models.ForeignKey(ChildAssent,on_delete=models.PROTECT)
    assent_fk = models.ForeignKey(Assent,on_delete=models.PROTECT)
    assent_date = models.DateField(default=timezone.now)
    assent_boolean = models.BooleanField(default=True, null=False, blank=False)

class AgeCategory(models.Model):

    class AgeCategoryChoice (models.TextChoices):
        EARLY_CHILDHOOD = 'EC', _('Early Childhood')
        MIDDLE_CHILDHOOD = 'MC', _('Middle Childhood')
        LATE_CHILDHOOD = 'LC', _('Late Childhood')
        ZERO_TO_FIVE = 'ZF', _('Zero to Five Months')
        TWELVE_TO_THIRTEEN_MONTHS = 'TT', _('Twelve to Thirteen Months')
        SIX_TO_TEN_YEARS = 'ST', _('Six to Ten Years')

    age_category = models.CharField(max_length=2,choices=AgeCategoryChoice.choices)

    def __str__(self):
        return f"{self.age_category}"


class CaregiverChildRelation(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    child_fk = models.ForeignKey(Child,on_delete=models.PROTECT)
    relation_fk = models.ForeignKey(Relation,on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','child_fk'],name="caregiver_child_relation_constraint")
        ]