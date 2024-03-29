from django.db import models
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

import logging
logging.basicConfig(level=logging.debug)

URINE = "U"
BLOOD_DICT_FORM = {'whole_blood': 'W',
                   'serum':'S',
                   'plasma':'P',
                   'red_blood_cells':'R',
                   'buffy_coat':'F',
                   }

BLOOD_DICT = {'Whole Blood': 'whole_blood',
              'Serum':'serum',
              'Plasma':'plasma',
              'Red Blood Cells':'red_blood_cells',
              'Buffy Coat':'buffy_coat'}

BLOOD_DICT_DISPLAY = {'whole_blood':'Whole Blood',
              'serum':'Serum',
              'plasma':'Plasma',
              'red_blood_cells':'Red Blood Cells',
              'buffy_coat':'Buffy Coat'}

class ComponentError(Exception):
    pass

class User(AbstractUser):
    class RecruitmentLocation(models.TextChoices):
        DETROIT = 'D', _('Detroit')
        TRAVERSE_CITY = 'T', _('Traverse City')
        FLINT = 'F', _('Flint')

    recruitment_location = models.CharField(max_length=1,choices=RecruitmentLocation.choices)
    is_staff = models.BooleanField('staff status',default=False)

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
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)


    def save_incentive(self,form,request):
        self.incentive_date = form.cleaned_data['incentive_date']
        self.logged_by = request.user
        self.save()

    def save_fk(self,caregiver_bio):
        caregiver_bio.incentive_fk = self
        caregiver_bio.save()
        self.save()

    def save_incentive_blood(self,bound_form,request):
        self.incentive_date = bound_form.cleaned_data['incentive_date']
        self.logged_by = request.user
        self.save()
        self.save()

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

    def create_collected_and_set_status_fk(self,caregiver_bio):
        caregiver_bio.status_fk.collected_fk = self
        caregiver_bio.status_fk.save()
        caregiver_bio.save()

    def save_urine(self,form,request):
        self.collected_date_time = form.cleaned_data['collected_date_time']
        self.processed_date_time = form.cleaned_data['processed_date_time']
        self.stored_date_time = form.cleaned_data['stored_date_time']
        self.number_of_tubes = form.cleaned_data['number_of_tubes']
        self.logged_by = request.user
        self.save()

    def save_hair_saliva(self,form,request):
        self.collected_date_time = form.cleaned_data['date_collected']
        self.in_person_remote = form.cleaned_data['in_person_remote']
        self.logged_by = request.user
        self.save()

    def save_placenta(self,form,request):
        self.collected_date_time = form.cleaned_data['collected_date_time']
        self.processed_date_time = form.cleaned_data['processed_date_time']
        self.placed_in_formalin_date_time = form.cleaned_data['placed_in_formalin']
        self.logged_by = request.user
        self.save()

    def save_blood(self,form,request):
        self.collected_date_time = form.cleaned_data['collected_date_time']
        self.processed_date_time = form.cleaned_data['processed_date_time']
        self.stored_date_time = form.cleaned_data['stored_date_time']
        self.logged_by = request.user
        self.save()

    def component_check(self,components,form):
        logging.debug(f"{form.cleaned_data}")

    class InpersonRemoteChoices(models.TextChoices):
        IN_PERSON = 'I', _('In Person')
        REMOTE = 'R', _('Remote')

    in_person_remote = models.CharField(max_length=1, choices=InpersonRemoteChoices.choices)

    ##todo check for formaline datetime if placenta

    def __str__(self):
        return f"collected {self.status_set}"

class NotCollected(models.Model):
    not_collected_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"collected {self.status_set}"

class NoConsent(models.Model):
    no_consent_datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

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

    def save_shipped_wsu(self,form,request,caregiver_bio,collection_type=None):
        self.shipped_date_time = form.cleaned_data['shipped_date_and_time']
        self.tracking_number = form.cleaned_data['tracking_number']
        self.courier = form.cleaned_data['courier']
        self.shipped_by = request.user
        if collection_type==URINE:
            self.number_of_tubes = form.cleaned_data['number_of_tubes']
        self.save()
        caregiver_bio.status_fk.shipped_wsu_fk = self
        caregiver_bio.status_fk.shipped_wsu_fk.save()
        caregiver_bio.status_fk.save()
        caregiver_bio.save()


    def __str__(self):
        return f"shippedwus  {self.pk}"

class ShippedECHO(models.Model):
    shipped_date_time = models.DateTimeField(null=True,blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)

    def set_shipped_date_time_and_fk_and_save(self,caregiver_bio,request,form):
        self.shipped_date_time = form.cleaned_data['shipped_date_and_time']
        self.logged_by = request.user
        caregiver_bio.status_fk.shipped_echo_fk = self
        self.save()
        caregiver_bio.status_fk.save()
        caregiver_bio.save()

    def __str__(self):
        return f"shipped {self.shipped_date_time}"

class KitSent(models.Model):
    kit_sent_date = models.DateField(null=True,blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save_form(self,form,request):
        self.kit_sent_date = form.cleaned_data['kit_sent_date']
        self.logged_by = request.user
        self.save()

    def __str__(self):
        return f"kit sent {self.kit_sent_date}"

class Declined(models.Model):
    declined_date = models.DateField(null=True,blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save_declined(self,form,request,caregiver_bio):
        self.declined_date = form.cleaned_data['declined_date_time']
        self.logged_by = request.user
        caregiver_bio.status_fk.declined_fk = self
        caregiver_bio.status_fk.save()
        caregiver_bio.save()
        self.save()

    def __str__(self):
        return f"declined date {self.declined_date}"

class ReceivedWSU(models.Model):
    received_date_time = models.DateTimeField(null=True,blank=True)
    number_of_tubes = models.IntegerField(default=None, null=True, blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,blank=True)

    def save_received_wsu(self,caregiver_bio,request,form=None):
        if caregiver_bio.collection_fk.collection_type=='B':
            self.received_date_time = form.cleaned_data['received_date_time']
            self.logged_by = request.user
        else:
            self.received_date_time = form.cleaned_data['received_date_time']
            self.logged_by = request.user
            self.number_of_tubes = form.cleaned_data['number_of_tubes']
        caregiver_bio.status_fk.received_wsu_fk = self
        caregiver_bio.status_fk.received_wsu_fk.save()
        caregiver_bio.status_fk.save()
        caregiver_bio.save()


    def __str__(self):
        return f"received date time {self.received_date_time}"

class ShippedMSU(models.Model):
    shipped_date_time = models.DateTimeField(null=True,blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save_msu_item(self,form,caregiver_bio,request):
        self.shipped_date_time = form.cleaned_data['shipped_date_time']
        self.logged_by = request.user
        caregiver_bio.status_fk.shipped_msu_fk = self
        self.save()
        caregiver_bio.status_fk.save()
        caregiver_bio.save()

    def __str__(self):
        return f"shipped {self.shipped_date_time}"

class ReceivedMSU(models.Model):
    received_date_time = models.DateTimeField(null=True, blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save_received_msu_item(self,form,caregiver_bio,request):
        self.received_date_time = form.cleaned_data['received_date_time']
        self.logged_by = request.user
        caregiver_bio.status_fk.received_msu_fk = self
        self.save()
        caregiver_bio.status_fk.save()
        caregiver_bio.save()

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

    def save_status(self,caregiver_bio):
        caregiver_bio.status_fk = self
        self.save()
        caregiver_bio.save()

    def save_initial_form(self,form,caregiver_bio,request):
        logging.debug(f"form name {request.POST}")
        if request.POST.__contains__('initial_form-collected_not_collected'):
            if form.cleaned_data['collected_not_collected'] == 'C':
                new_collected = Collected.objects.create()
                self.collected_fk = new_collected
                new_collected.save()
            elif form.cleaned_data['collected_not_collected'] == 'N':
                new_not_collected = NotCollected.objects.create()
                new_not_collected.logged_by = request.user
                self.not_collected_fk = new_not_collected
                new_not_collected.save()
            elif form.cleaned_data['collected_not_collected'] == 'X':
                logging.debug(f"In declined form")
                new_declined = Declined.objects.create()
                self.declined_fk = new_declined
                new_declined.save()
        elif request.POST.__contains__('initial_form-collected_not_collected_kit_sent'):
            if form.cleaned_data['collected_not_collected_kit_sent'] == 'K':
                new_kit_sent = KitSent.objects.create()
                self.kit_sent_fk = new_kit_sent
            elif form.cleaned_data['collected_not_collected_kit_sent'] == 'N':
                new_not_collected = NotCollected.objects.create()
                new_not_collected.logged_by = request.user
                self.not_collected_fk = new_not_collected
                new_not_collected.save()
            elif form.cleaned_data['collected_not_collected_kit_sent'] == 'X':
                new_declined = Declined.objects.create()
                self.declined_fk = new_declined
        elif request.POST.__contains__('initial_form-collected_not_collected_no_consent'):
            if form.cleaned_data['collected_not_collected_no_consent'] == 'O':
                new_no_consent = NoConsent.objects.create()
                self.no_consent_fk = new_no_consent
            elif form.cleaned_data['collected_not_collected_no_consent'] == 'C':
                new_collected = Collected.objects.create()
                self.collected_fk = new_collected
            elif form.cleaned_data['collected_not_collected_no_consent'] == 'N':
                new_not_collected = NotCollected.objects.create()
                new_not_collected.logged_by = request.user
                self.not_collected_fk = new_not_collected
                new_not_collected.save()
        else:
            raise KeyError
        self.save_status(caregiver_bio=caregiver_bio)

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
        BLOODSPOT = 'S', _('Bloodspot')

    collection_type = models.CharField(max_length=1,choices=CollectionType.choices)
    collection_number = models.IntegerField(default=None,null=True,blank=True)

    def __str__(self):
        return f"{self.collection_type}"


class Caregiver(models.Model):
    charm_project_identifier = models.CharField(default='', max_length=6,unique=True)

    class Cohort(models.TextChoices):
        DETROIT = 'D',_('Detroit')
        TRAVERSE_CITY = 'T',_('Traverse City')
        FLINT = 'F',_('Flint')

    recruitment_location = models.CharField(max_length=1,choices=Cohort.choices)

    def check_recruitment(self,request,caregiver=None):
        if (request.user.is_staff) or (caregiver.recruitment_location==request.user.recruitment_location):
            return True
        elif (caregiver.recruitment_location!=request.user.recruitment_location):
            raise PermissionError

    def __str__(self):
        return self.charm_project_identifier

class PregnancyTrimester(models.Model):
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

    def __str__(self):
        return f"pregnancy: {self.pregnancy_number}"

class Perinatal(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    pregnancy_fk = models.OneToOneField(Pregnancy,on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk', 'pregnancy_fk'], name="perinatal_unique_constraint")
        ]

    def __str__(self):
        return f"birth event: {self.caregiver_fk.charm_project_identifier} {self.pregnancy_fk.pregnancy_number}"

class Child(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver, on_delete=models.PROTECT)
    pregnancy_fk = models.ForeignKey(Pregnancy,on_delete=models.PROTECT)
    charm_project_identifier = models.CharField(max_length=6, unique=True)

    def __string__(self):
        return f"child: {self.charm_project_identifier}"

class CaregiverBiospecimen(models.Model):
    caregiver_fk = models.ForeignKey(Caregiver,on_delete=models.PROTECT)
    status_fk = models.OneToOneField(Status, on_delete=models.PROTECT, blank=True,null=True)
    collection_fk = models.ForeignKey(Collection, on_delete=models.PROTECT)
    incentive_fk = models.ForeignKey(Incentive, on_delete=models.PROTECT,blank=True,null=True)
    trimester_fk = models.ForeignKey(PregnancyTrimester,on_delete=models.PROTECT,blank=True,null=True)
    pregnancy_fk = models.ForeignKey(Pregnancy,on_delete=models.PROTECT,blank=True,null=True)
    perinatal_fk = models.ForeignKey(Perinatal,on_delete=models.PROTECT,blank=True,null=True)
    age_category_fk = models.ForeignKey(AgeCategory,on_delete=models.PROTECT,blank=True,null=True)
    project_fk = models.ForeignKey(Project,on_delete=models.PROTECT,blank=False,null=False)
    biospecimen_id = models.CharField(max_length=10, null=False,blank=False,unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_fk','collection_fk','trimester_fk'], name='caregiver biospecimen unique constraint')
        ]

    def check_recruitment(self,request,caregiver_bio=None,caregiver_charm_id=None):
        caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
        if(caregiver_bio.caregiver_fk.charm_project_identifier!=caregiver_charm_id):
            raise PermissionError
        if (request.user.is_staff) or (caregiver_bio.caregiver_fk.recruitment_location==request.user.recruitment_location) \
                or (caregiver.recruitment_location==request.user.recruitment_location):
            return True
        elif (caregiver_bio.caregiver_fk.recruitment_location!=request.user.recruitment_location) \
                or (caregiver.recruitment_location!=request.user.recruitment_location):
            raise PermissionError

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
    collected_fk = models.ForeignKey(Collected,on_delete=models.PROTECT,null=True,blank=True)
    shipped_wsu_fk = models.ForeignKey(ShippedWSU,on_delete=models.PROTECT,null=True,blank=True)
    received_wsu_fk = models.ForeignKey(ReceivedWSU,on_delete=models.PROTECT,null=True,blank=True)
    shipped_echo_fk = models.ForeignKey(ShippedECHO,on_delete=models.PROTECT,null=True,blank=True)

    class ComponentType(models.TextChoices):
        SERUM = 'S',_('Serum')
        PLASMA = 'P',_('Plasma')
        BLOODSPOTS = 'D', _('Bloodspots')
        WHOLEBLOOD = 'W', _('Whole Blood')
        BUFFYCOAT = 'F', _('Buffy Coat')
        REDBLOODCELLS = 'R', _('Red Blood Cells')

    component_type = models.CharField(max_length=1,choices=ComponentType.choices)
    number_of_tubes = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caregiver_biospecimen_fk','component_type',], name='component unique constraint')
        ]

    def whole_blood_number_of_tubes(self):
        pass

    def __str__(self):
        return f"{self.get_component_type_display()}"