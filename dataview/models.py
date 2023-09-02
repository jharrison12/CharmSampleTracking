import datetime
from django.utils import timezone
from django.db import models
import pytz
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Caregiver(models.Model):
    #caregiver_pk = models.AutoField(primary_key=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address_line_1','address_line_2','city','state','zip_code'],name=f"address_unique_constraint")
        ]

class CaregiverAddress(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','address_fk'],name="caregiver_address_constraint")
        ]

class AddressMove(models.Model):
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)
    address_move_date = models.DateField(blank=False,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address_fk','address_move_date'],name="address_move_unique_constraint")
        ]

class CaregiverAddressHistory(models.Model):
    caregiver_address_fk = models.ForeignKey(CaregiverAddress,on_delete=models.PROTECT)
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)
    revision_number = models.IntegerField()
    revision_date = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_address_fk','caregiver_fk','address_fk','revision_number'],
                                    name="caregiver_address_history_unique_constraint")
        ]

class Email(models.Model):
    email = models.EmailField(null=True,unique=True)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email_fk','caregiver_fk','email_type'],
                                    name="caregiver_email_unique_constraint")
        ]

class Phone(models.Model):
    area_code = models.CharField(null=False,blank=False,max_length=3)
    phone_number = models.CharField(null=False,blank=False,max_length=8)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk', 'phone_fk','phone_type'],
                                    name="caregiver_phone_unique_constraint")
        ]

class SocialMedia(models.Model):
    social_media_name = models.CharField(null=True,blank=True,max_length=255,unique=True)

class CaregiverSocialMedia(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    social_media_fk = models.ForeignKey(SocialMedia,on_delete=models.PROTECT)
    social_media_user_name = models.CharField(null=False,blank=False,max_length=255)
    social_media_consent = models.BooleanField(default=True)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['incentive_type_fk','incentive_amount'],name="incentive_unique_constraint")
        ]

    def __str__(self):
        return f"{self.incentive_type_fk}: {self.incentive_amount}"

class Project(models.Model):
    project_name = models.CharField(null=False, blank=False, max_length=255,unique=True)

class Survey(models.Model):
    project_fk = models.ForeignKey(Project, on_delete=models.PROTECT)
    survey_name = models.CharField(null=False, blank=False, max_length=255,unique=True)

class SurveyOutcome(models.Model):
    survey_outcome_text = models.CharField(null=False, blank=False, max_length=255,unique=True)

class CaregiverSurvey(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    survey_fk = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_outcome_fk = models.ForeignKey(SurveyOutcome, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive,on_delete=models.PROTECT)
    survey_completion_date = models.DateField(blank=False, null=False, default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','survey_fk'],name="caregiver_survey_unique_constraint")
        ]

class HealthcareFacility(models.Model):
    name = models.CharField(null=False,blank=False,max_length=255,unique=True)

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
    due_date = models.DateField(null=False,blank=False)

class Relation(models.Model):
    relation_type = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.relation_type

class NonMotherCaregiver(models.Model):
    caregiver_fk = models.OneToOneField(Caregiver,on_delete=models.PROTECT)
    relation_fk = models.ForeignKey(Relation,on_delete=models.PROTECT)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','relation_fk'],name="non_mother_caregiver_unqiue_constraint")
        ]

class Status(models.Model):
    #todo sublcass text choices for status
    status = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.status

class Collection(models.Model):
    #todo subclass text choices
    collection_type = models.CharField(max_length=255)
    collection_number = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.collection_type} {self.collection_number}"

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['collection_type','collection_number'],name="collection_unique_constraint")
        ]

class CaregiverBiospecimen(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    status_fk = models.ForeignKey(Status, on_delete=models.PROTECT)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT)
    biospecimen_date = models.DateField(blank=False,null=False,default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk'],name="caregiver_biospecimen_unique_constraint")
        ]