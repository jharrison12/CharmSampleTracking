from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
import logging
logging.basicConfig(level=logging.debug)

# Create your models here.

class User(AbstractUser):
    pass

class Project(models.Model):
    project_name = models.CharField(null=False, blank=False, max_length=255,unique=True)

    def __str__(self):
        return f"{self.project_name}"

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


class Incentive(models.Model):
    class IncentiveType(models.TextChoices):
        GIFT_CARD = 'G', _('Gift Card')
        CASH = 'C', _('Cash')
        CHECK = 'H', _('Check')
    incentive_type = models.CharField(max_length=1,choices=IncentiveType.choices)
    incentive_date = models.DateField(blank=True,null=True)
    incentive_amount =models.IntegerField(null=True)

    def __str__(self):
        return f"{self.incentive_type}: {self.incentive_amount}"


class Collected(models.Model):
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,null=True,blank=True)
    collected_date_time = models.DateTimeField(null=True,blank=True)
    processed_date_time = models.DateTimeField(null=True,blank=True)
    stored_date_time = models.DateTimeField(null=True,blank=True)
    number_of_tubes = models.IntegerField(null=True,blank=True)
    placed_in_formalin_date_time = models.DateTimeField(null=True,blank=True)
    received_date = models.DateField(null=True,blank=True)
    number_of_cards = models.IntegerField(null=True,blank=True)

    class InpersonRemoteChoices(models.TextChoices):
        IN_PERSON = 'I', _('In Person')
        REMOTE = 'R', _('Remote')

    in_person_remote = models.CharField(max_length=1, choices=InpersonRemoteChoices.choices)

    ##todo check for formaline datetime if placenta

    def __str__(self):
        return f"collected {self.status_set}"

class NotCollected(models.Model):
    not_collected_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)

    def __str__(self):
        return f"collected {self.status_set}"

class NoConsent(models.Model):
    no_consent_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)

    def __str__(self):
        return f"collected {self.status_set}"

class ShippedWSU(models.Model):
    shipped_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)
    shipped_date_time = models.DateTimeField(null=True,blank=True)
    number_of_tubes = models.IntegerField(default=None,null=True,blank=True)
    tracking_number = models.CharField(max_length=255,null=True,blank=True)

    class CourierChoices(models.TextChoices):
        FEDEX = 'F', _('FedEx')
        USPS = 'P', _('USPS')
        UPS = 'U', _('UPS')
        DHL = 'D', _('DHL')

    courier = models.CharField(max_length=1,choices=CourierChoices.choices,null=True,blank=True)

    def __str__(self):
        return f"shippedwus  {self.pk}"

class ShippedECHO(models.Model):
    shipped_date_time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"shipped {self.shipped_date_time}"

class KitSent(models.Model):
    kit_sent_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"kit sent {self.kit_sent_date}"

class Declined(models.Model):
    declined_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"declined date {self.declined_date}"

class ReceivedWSU(models.Model):
    received_date_time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"received date time {self.received_date_time}"

class ShippedMSU(models.Model):
    shipped_date_time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"shipped {self.shipped_date_time}"

class ReceivedMSU(models.Model):
    received_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"received {self.received_date_time}"

class Status(models.Model):
    #todo sublcass text choices for status
    kit_sent_fk = models.ForeignKey(KitSent,on_delete=models.PROTECT, blank=True,null=True)
    collected_fk = models.ForeignKey(Collected, on_delete=models.PROTECT, null=True, blank=True)
    shipped_wsu_fk = models.ForeignKey(ShippedWSU,on_delete=models.PROTECT,null=True,blank=True)
    received_wsu_fk = models.ForeignKey(ReceivedWSU,on_delete=models.PROTECT,null=True,blank=True)
    shipped_msu_fk = models.ForeignKey(ShippedMSU,on_delete=models.PROTECT,null=True,blank=True)
    received_msu_fk = models.ForeignKey(ReceivedMSU,on_delete=models.PROTECT,null=True,blank=True)
    shipped_echo_fk = models.ForeignKey(ShippedECHO,on_delete=models.PROTECT,null=True,blank=True)
    not_collected_fk = models.ForeignKey(NotCollected, on_delete=models.PROTECT, null=True, blank=True)
    no_consent_fk = models.ForeignKey(NoConsent,on_delete=models.PROTECT,null=True,blank=True)
    declined_fk = models.ForeignKey(Declined,on_delete=models.PROTECT,blank=True,null=True)

    def return_most_up_to_date_status(self):
        if self.received_fk and self.received_fk.outcome_fk.get_outcome_display()=='C':
            return f"Received: {self.received_fk.outcome_fk.get_outcome_display()}"
        elif self.shipped_fk and self.shipped_fk.outcome_fk.get_outcome_display()=='C':
            return f"Shipped: {self.shipped_fk.outcome_fk.get_outcome_display()}"
        elif self.stored_fk and self.stored_fk.outcome_fk.get_outcome_display()=='C':
            return f"Stored: {self.shipped_fk.outcome_fk.get_outcome_display()}"
        elif self.processed_fk and self.processed_fk.outcome_fk.get_outcome_display()=='C':
            return f"Processed: {self.shipped_fk.outcome_fk.get_outcome_display()}"
        else:
            return None

    def __str__(self):
        return f"Status {self.pk}"

    class Meta:
        verbose_name_plural = "status"


class Collection(models.Model):
    #todo subclass text choices
    class CollectionType(models.TextChoices):
        URINE = 'U',_('Urine')
        HAIR = 'H', _('Hair')
        TOENAIL = 'T', _('Toenail')
        SALIVA = 'L', _('Saliva')
        PLACENTA = 'C', _('Placenta')
        STOOL = 'O', _('Stool')
        TOOTH = 'E', _('Tooth')
        CORDBLOOD = 'X', _('Cord Blood')
        BLOOD = 'B', _('Blood')

    collection_type = models.CharField(max_length=1,choices=CollectionType.choices)

    def __str__(self):
        return f"{self.collection_type}"


class Caregiver(models.Model):
    charm_project_identifier = models.CharField(default='', max_length=6,unique=True)

    def __str__(self):
        return self.charm_project_identifier

class Trimester(models.Model):
    pregnancy_fk = models.ForeignKey("Pregnancy",on_delete=models.PROTECT)
    class TrimesterChoices(models.TextChoices):
        FIRST = 'F',_('First')
        SECOND = 'S', _('Second')
        THIRD = 'T',_('Third')
    trimester = models.CharField(max_length=1,choices=TrimesterChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pregnancy_fk', 'trimester'], name="trimester_unique_constraint")
        ]


    def __str__(self):
        return f"{self.get_trimester_display()}"

class Pregnancy(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    pregnancy_number = models.IntegerField(null=False,default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk', 'pregnancy_number'], name="pregnancy_unique_constraint")
        ]

    def __string__(self):
        return f"pregnancy: {self.pregnancy_number}"

class Child(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    pregnancy_fk = models.ForeignKey(Pregnancy,on_delete=models.PROTECT)
    charm_project_identifier = models.CharField(max_length=6, unique=True)

class Perinatal(models.Model):
    #perinatal event like birth
    #i need this table to capture multiple placentas associated with one birth
    pregnancy_fk = models.ForeignKey(Pregnancy,null=False,blank=False,on_delete=models.PROTECT)
    child_fk = models.OneToOneField(Child,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.pregnancy_fk.pregnancy_id}"

class CaregiverBiospecimen(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    status_fk = models.OneToOneField(Status, on_delete=models.PROTECT, blank=True,null=True)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    trimester_fk = models.ForeignKey(Trimester,on_delete=models.PROTECT,blank=True,null=True)
    perinatal_fk = models.ForeignKey("Perinatal",on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory,on_delete=models.PROTECT,blank=True,null=True)
    project_fk = models.ForeignKey(Project,on_delete=models.PROTECT,blank=False,null=False)
    biospecimen_id = models.CharField(max_length=10, null=False,blank=False,unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk','trimester_fk'], name='caregiver biospecimen unique constraint')
        ]


    def __str__(self):
        return f"{self.caregiver_fk.charm_project_identifier} {self.biospecimen_id}"

class ChildBiospecimen(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    status_fk = models.ForeignKey(Status, on_delete=models.PROTECT, null=True,blank=True)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory, on_delete=models.PROTECT)
    biospecimen_id = models.CharField(max_length=10, null=True,blank=False,unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['collection_fk','age_category_fk',], name='child biospeciment unique constraint')
        ]

    def __str__(self):
        return f"{self.biospecimen_id}"

class Component(models.Model):
    caregiver_biospecimen_fk = models.ForeignKey(CaregiverBiospecimen,on_delete=models.PROTECT)
    class ComponentType(models.TextChoices):
        SERUM = 'S',_('Serum')
        PLASMA = 'P',_('Plasma')
        BLOODSPOTS = 'D', _('Bloodspots')
        WHOLEBLOOD = 'W', _('Whole Blood')
        BUFFYCOAT = 'F', _('Buffy Coat')
        REDBLOODCELLS = 'R', _('Red Blood Cells')

    component_type = models.CharField(max_length=1,choices=ComponentType.choices)
    number_of_tubes = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.component_type}"