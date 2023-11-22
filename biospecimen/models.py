from django.db import models
from dataview.models import Caregiver,Incentive,Child,AgeCategory,Pregnancy,Project,User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import logging
logging.basicConfig(level=logging.debug)

# Create your models here.

class Outcome(models.Model):
    class OutcomeChoices(models.TextChoices):
        COMPLETED = 'C', _('Completed')
        IN_PROCESS = 'P', _('In Process')
        NOT_COLLECTED = 'N', _('Not Collected')

    outcome = models.CharField(max_length=1,unique=True,choices=OutcomeChoices.choices)

    def __str__(self):
        return self.outcome

class Received(models.Model):
    ##todo add user
    outcome_fk = models.ForeignKey(Outcome, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    #todo sublcass storage
    storage_location = models.CharField(max_length=255)
    received_date_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    logged_date_time = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"received {self.outcome_fk.get_outcome_display()}"

class Shipped(models.Model):
    ##todo add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    #subclass this
    courier = models.CharField(max_length=255)
    shipping_number = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    shipped_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return f"shipped {self.outcome_fk.get_outcome_display()}"

class Stored(models.Model):
    ##TODO add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    stored_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    #todo subclass this
    storage_location = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return f"stored {self.outcome_fk.get_outcome_display()}"

class Processed(models.Model):
    #TODO add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    collected_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    processed_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return f"processed {self.outcome_fk.get_outcome_display()}"

class Collected(models.Model):
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,null=True,blank=True)
    collected_date_time = models.DateTimeField(null=True,blank=True)
    processed_date_time = models.DateTimeField(null=True,blank=True)
    stored_date_time = models.DateTimeField(null=True,blank=True)
    placed_in_formalin_date_time = models.DateTimeField(null=True,blank=True)
    received_date = models.DateField(null=True,blank=True)
    number_of_tubes = models.IntegerField(null=True,blank=True)
    number_of_cards = models.IntegerField(null=True,blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)

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
    shipped_date_time = models.DateTimeField(null=True,blank=True)
    number_of_tubes = models.IntegerField(default=None,null=True,blank=True)
    tracking_number = models.CharField(max_length=255,null=True,blank=True)
    shipped_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)
    logged_date_time = models.DateTimeField(default=timezone.now,blank=True,null=True)

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
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return f"collected {self.status_set}"

class KitSent(models.Model):
    kit_sent_date = models.DateField(null=True,blank=True)

class Declined(models.Model):
    declined_date = models.DateField(null=True,blank=True)

class ReceivedWSU(models.Model):
    received_date_time = models.DateTimeField(null=True,blank=True)

class Status(models.Model):
    #todo sublcass text choices for status
    processed_fk = models.ForeignKey(Processed,on_delete=models.PROTECT,null=True,blank=True)
    stored_fk = models.ForeignKey(Stored,on_delete=models.PROTECT,null=True,blank=True)
    shipped_fk = models.ForeignKey(Shipped,on_delete=models.PROTECT,null=True,blank=True)
    received_fk = models.ForeignKey(Received, on_delete=models.PROTECT, null=True, blank=True)
    collected_fk = models.ForeignKey(Collected, on_delete=models.PROTECT, null=True, blank=True)
    not_collected_fk = models.ForeignKey(NotCollected, on_delete=models.PROTECT, null=True, blank=True)
    no_consent_fk = models.ForeignKey(NoConsent,on_delete=models.PROTECT,null=True,blank=True)
    shipped_wsu_fk = models.ForeignKey(ShippedWSU,on_delete=models.PROTECT,null=True,blank=True)
    received_wsu_fk = models.ForeignKey(ReceivedWSU,on_delete=models.PROTECT,null=True,blank=True)
    shipped_echo_fk = models.ForeignKey(ShippedECHO,on_delete=models.PROTECT,null=True,blank=True)
    kit_sent_fk = models.ForeignKey(KitSent,on_delete=models.PROTECT, blank=True,null=True)
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

class CollectionType(models.Model):
    collection_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.collection_type}"

class CollectionNumber(models.Model):
    class CollectionNumberChoices(models.TextChoices):
        FIRST = 'F',_('First')
        SECOND = 'S',_('Second')
        THIRD = 'T',_('Third')
        EARLY_CHILDHOOD = 'EC',_('Early Childhood')
        MIDDLE_CHILDHOOD = 'MC',_('Middle Childhood')
    collection_number = models.CharField(max_length=2,choices=CollectionNumberChoices.choices)

    def __str__(self):
        return f"{self.collection_number}"

class Collection(models.Model):
    #todo subclass text choices
    collection_type_fk = models.ForeignKey(CollectionType,on_delete=models.PROTECT)
    collection_number_fk = models.ForeignKey(CollectionNumber,on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return f"{self.collection_type_fk.collection_type} {self.collection_number_fk or ''}"

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['collection_type_fk','collection_number_fk'],name="collection_unique_constraint")
        ]

class Trimester(models.Model):
    pregnancy_fk = models.ForeignKey(Pregnancy,on_delete=models.PROTECT)
    class TrimesterChoices(models.TextChoices):
        FIRST = 'F',_('First')
        SECOND = 'S', _('Second')
        THIRD = 'T',_('Third')
    trimester = models.CharField(max_length=1,choices=TrimesterChoices.choices)

    def __str__(self):
        return f"{self.get_trimester_display()}"

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
    perinatal_fk = models.ForeignKey(Perinatal,on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory,on_delete=models.PROTECT,blank=True,null=True)
    project_fk = models.ForeignKey(Project,on_delete=models.PROTECT,blank=False,null=False)
    biospecimen_id = models.CharField(max_length=7, null=False,blank=False,unique=True)
    biospecimen_date = models.DateField(blank=False,null=False,default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk','trimester_fk'],
                                    name="caregiver_biospecimen_unique_constraint",
                                    violation_error_message="You can't have a duplicate item")
        ]

    def __str__(self):
        return f"{self.caregiver_fk.charm_project_identifier} {self.biospecimen_id}"


class ChildBiospecimen(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    status_fk = models.ForeignKey(Status, on_delete=models.PROTECT, null=True,blank=True)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory, on_delete=models.PROTECT)
    collection_date = models.DateField(default=timezone.now)
    biospecimen_id = models.CharField(max_length=7, null=True,blank=False,unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child_fk','collection_fk','age_category_fk'], name='child biospeciment unique constraint')
        ]

    def __str__(self):
        return f"{self.child_fk.charm_project_identifier} {self.collection_fk}"


