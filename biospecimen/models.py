from django.db import models
from dataview.models import Caregiver,Incentive,Child,AgeCategory,Pregnancy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import logging
logging.basicConfig(level=logging.CRITICAL)

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

class Shipped(models.Model):
    ##todo add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    #subclass this
    courier = models.CharField(max_length=255)
    shipping_number = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    shipped_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

class Stored(models.Model):
    ##TODO add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    stored_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    #todo subclass this
    storage_location = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

class Processed(models.Model):
    #TODO add user
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT,null=True,blank=True)
    collected_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    processed_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)


class Collected(models.Model):
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,null=True,blank=True)
    collected_date_time = models.DateTimeField(null=True,blank=True)
    processed_date_time = models.DateTimeField(null=True,blank=True)
    stored_date_time = models.DateTimeField(null=True,blank=True)
    placed_in_formalin_date_time = models.DateTimeField(null=True,blank=True)
    received_date = models.DateField(null=True,blank=True)
    number_of_tubes = models.IntegerField(null=True,blank=True)

    class InpersonRemoteChoices(models.TextChoices):
        IN_PERSON = 'I', _('In Person')
        REMOTE = 'R', _('Remote')

    in_person_remote = models.CharField(max_length=1, choices=InpersonRemoteChoices.choices)

    ##todo check for formaline datetime if placenta

class NotCollected(models.Model):
    not_collected_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)

class NoConsent(models.Model):
    no_consent_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)


class Status(models.Model):
    #todo sublcass text choices for status
    processed_fk = models.ForeignKey(Processed,on_delete=models.PROTECT,null=True,blank=True)
    stored_fk = models.ForeignKey(Stored,on_delete=models.PROTECT,null=True,blank=True)
    shipped_fk = models.ForeignKey(Shipped,on_delete=models.PROTECT,null=True,blank=True)
    received_fk = models.ForeignKey(Received, on_delete=models.PROTECT, null=True, blank=True)
    collected_fk = models.ForeignKey(Collected, on_delete=models.PROTECT, null=True, blank=True)
    not_collected_fk = models.ForeignKey(NotCollected, on_delete=models.PROTECT, null=True, blank=True)
    no_consent_fk = models.ForeignKey(NoConsent,on_delete=models.PROTECT,null=True,blank=True)

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
            logging.debug(f"{self.received_fk} {self.objects.model}")
            return None

    def __str__(self):
        return f"{self.processed_fk}"

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
        return f"{self.collection_type_fk.collection_type} {self.collection_number_fk.collection_number or ''}"

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

class Perinatal(models.Model):
    #perinatal event like birth
    #i need this table to capture multiple placentas associated with one birth
    pregnancy_fk = models.ForeignKey(Pregnancy,null=False,blank=False,on_delete=models.PROTECT)
    child_fk = models.OneToOneField(Child,on_delete=models.PROTECT)



class CaregiverBiospecimen(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    status_fk = models.OneToOneField(Status, on_delete=models.PROTECT, blank=True,null=True)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    trimester_fk = models.ForeignKey(Trimester,on_delete=models.PROTECT,blank=True,null=True)
    perinatal_fk = models.ForeignKey(Perinatal,on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory,on_delete=models.PROTECT,blank=True,null=True)
    biospecimen_id = models.CharField(max_length=7, null=False,blank=False,unique=True)
    biospecimen_date = models.DateField(blank=False,null=False,default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk','trimester_fk'],
                                    name="caregiver_biospecimen_unique_constraint",
                                    violation_error_message="You can't have a duplicate item")
        ]


class ChildBiospecimen(models.Model):
    child_fk = models.ForeignKey(Child, on_delete=models.PROTECT)
    status_fk = models.ForeignKey(Status, on_delete=models.PROTECT)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory, on_delete=models.PROTECT)
    collection_date = models.DateField(default=timezone.now)
    kit_sent_date = models.DateField(default=timezone.now,blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child_fk','collection_fk','age_category_fk'], name='child biospeciment unique constraint')
        ]

    def __str__(self):
        return f"{self.child_fk.charm_project_identifier} {self.collection_fk}"

