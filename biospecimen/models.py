from django.db import models
from dataview.models import Caregiver,Incentive,Child,AgeCategory
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Outcome(models.Model):
    class OutcomeChoices(models.TextChoices):
        COMPLETED = 'C', _('Completed')
        IN_PROCESS = 'P', _('In Process')
        NOT_COLLECTED = 'N', _('Not Collected')

    outcome = models.CharField(max_length=1,unique=True,choices=OutcomeChoices.choices)

    def __str__(self):
        return self.outcome

class Processed(models.Model):
    #TODO add user
    collected_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    processed_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    logged_date_time = models.DateTimeField(default=timezone.now,null=True,blank=True)

class Status(models.Model):
    #todo sublcass text choices for status
    outcome_fk = models.ForeignKey(Outcome,on_delete=models.PROTECT)
    processed_fk = models.ForeignKey(Processed,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.outcome_fk}"

class Collection(models.Model):
    #todo subclass text choices
    collection_type = models.CharField(max_length=255)
    collection_number = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.collection_type} {self.collection_number or ''}"

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['collection_type','collection_number'],name="collection_unique_constraint")
        ]


class CaregiverBiospecimen(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    status_fk = models.ForeignKey(Status, on_delete=models.PROTECT)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    biospecimen_date = models.DateField(blank=False,null=False,default=timezone.now)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk'],
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