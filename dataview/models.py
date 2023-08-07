import datetime
from django.utils import timezone
from django.db import models
import pytz
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Caregiver(models.Model):
    #caregiver_pk = models.AutoField(primary_key=True)
    charm_project_identifier = models.CharField(default='', max_length=6)
    date_of_birth = models.DateField(blank=True, null=True)
    ewcp_participant_identifier = models.CharField(default='',max_length=16)
    participation_level_identifier = models.CharField(default='',max_length=2)
    echo_pin = models.CharField(default='',max_length=3)
    specimen_id = models.CharField(null=False,max_length=4,default='0000')


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

class Address(models.Model):
    address_line_1 = models.CharField(default='', max_length=255)
    address_line_2 = models.CharField(default='', max_length=255)
    city = models.CharField(default='', max_length=255)
    state = models.CharField(default='MI', max_length=2)
    zip_code = models.CharField(default='',max_length=9)

class CaregiverAddress(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)

class AddressMove(models.Model):
    address_fk = models.ForeignKey(Address,on_delete=models.PROTECT)
    address_move_date = models.DateField(blank=False,null=False)

class Email(models.Model):
    email = models.EmailField(null=True)

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

class Phone(models.Model):
    area_code = models.CharField(null=False,blank=False,max_length=3)
    phone_number = models.CharField(null=False,blank=False,max_length=8)

class CaregiverPhone(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    phone_fk = models.ForeignKey(Phone,on_delete=models.PROTECT)

    class CaregiverPhoneTypeChoices(models.TextChoices):
        PRIMARY = 'PR',_('Primary')
        SECONDARY = 'SD',_('Secondary')
        INACTIVE = 'IN',_('Inactive')

    phone_type = models.CharField(max_length=2,choices=CaregiverPhoneTypeChoices.choices,default=CaregiverPhoneTypeChoices.PRIMARY)
    date_change = models.DateField(blank=False,null=False,default=timezone.now)

class SocialMedia(models.Model):
    social_media_name = models.CharField(null=True,blank=True,max_length=255)

class CaregiverSocialMedia(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    social_media_fk = models.OneToOneField(SocialMedia,on_delete=models.PROTECT)
    social_media_user_name = models.CharField(null=False,blank=False,max_length=255)
    social_media_consent = models.BooleanField(default=True)