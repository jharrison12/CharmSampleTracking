import datetime

from django import forms
from dataview.models import Incentive
from biospecimen.models import CaregiverBiospecimen,Processed,Status
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone

CHOICES = [('C','Complete')]
IN_PERSON_REMOTE = [('I','In Person'),('R','Remote')]
COLLECTED_NOT = [('C','Collected'),('N','Not Collected'),('X','No Consent')]
KIT_SENT_NOT = [('K','Kit Sent'),('N','Not Collected'),('X','No Consent')]
SHIPPED_CHOICE = [('W','Shipped to WSU'),('E','Shipped to Echo')]
COURIERS = [('F','FedEx'),('P','USPS'),('U','UPS'),('D','DHL')]

class ReceivedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    quantity = forms.IntegerField()
    received_date_time = forms.DateTimeField(initial=timezone.now())
    logged_date_time = forms.DateTimeField()
    storage_location = forms.CharField()

class ShippedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    shipping_number = forms.CharField()
    quantity = forms.IntegerField()
    shipped_date_time = forms.DateTimeField(initial=timezone.now())
    logged_date_time = forms.DateTimeField()
    courier = forms.CharField()


class StoredBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select,choices=CHOICES)
    stored_date_time = forms.DateTimeField(initial=timezone.now())
    storage_location = forms.CharField()
    quantity = forms.IntegerField()
    logged_date_time = forms.DateTimeField()

class ProcessedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select,choices=CHOICES)
    collected_date_time = forms.DateTimeField(initial=timezone.now())
    processed_date_time = forms.DateTimeField()
    quantity = forms.IntegerField()
    logged_date_time = forms.DateTimeField()

class CaregiverBiospecimenForm(forms.models.ModelForm):

    # def save(self, caregiver_charm_fk_id):
    #     self.instance.caregiver_fk = caregiver_charm_fk_id
    #     return super().save()

    def clean(self):
        cd = self.cleaned_data
        if self.non_field_errors():
            self.add_error('caregiver_fk','this doesn\'t work')
        return cd

    class Meta:
        model = CaregiverBiospecimen
        fields = ['caregiver_fk','collection_fk','status_fk','biospecimen_date']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': f"This type of biospecimen for this charm id already exists",
            }
        }
        widgets = {
            "caregiver_fk": forms.HiddenInput(),
            "incentive_fk": forms.HiddenInput()
        }
        #exclude = ('incentive_fk',)

class IncentiveForm(forms.models.ModelForm):

    class Meta:
        model = Incentive
        fields = ['incentive_type_fk','incentive_date','incentive_amount']

class CollectedBiospecimenForm(forms.Form):
    collected_date_time = forms.DateTimeField()
    processed_date_time = forms.DateTimeField()
    stored_date_time = forms.DateTimeField()
    placed_in_formalin = forms.DateTimeField()
    received_date = forms.DateField()
    number_of_tubes = forms.IntegerField()
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)

class CollectedBiospecimenUrineForm(forms.Form):
    collected_date_time = forms.DateTimeField(initial=timezone.now())
    processed_date_time = forms.DateTimeField()
    stored_date_time = forms.DateTimeField()
    number_of_tubes = forms.IntegerField()

    class Meta:
        fields = ['collected_date_time','processed_date_time','stored_date_time','number_of_tubes']
        widgets = {
            "collected_date_time": forms.DateTimeInput,
            "processed_date_time": forms.DateTimeInput
        }

class InitialBioForm(forms.Form):
    collected_not_collected = forms.ChoiceField(widget=forms.Select,choices=COLLECTED_NOT)

class InitialBioFormChild(forms.Form):
    collected_not_collected_kit_sent = forms.ChoiceField(widget=forms.Select,choices=KIT_SENT_NOT)


class ShippedChoiceForm(forms.Form):
    shipped_to_wsu_or_echo = forms.ChoiceField(widget=forms.Select,choices=SHIPPED_CHOICE)

class ShippedtoWSUForm(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now())
    tracking_number = forms.CharField()
    number_of_tubes = forms.IntegerField()
    logged_date_time = forms.DateTimeField()
    courier = forms.ChoiceField(widget=forms.Select,choices=COURIERS)

class ShippedtoEchoForm(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now())


class CollectedBloodForm(forms.Form):
    collected_date_time = forms.DateTimeField(initial=timezone.now())
    processed_date_time = forms.DateTimeField()
    stored_date_time = forms.DateTimeField()
    number_of_tubes = forms.IntegerField()
    whole_blood = forms.BooleanField(required=False)
    plasma = forms.BooleanField(required=False)
    buffy_coat = forms.BooleanField( required=False)
    red_blood_cells = forms.BooleanField( required=False)
    serum = forms.BooleanField( required=False)

    class Meta:
        fields = ['collected_date_time','processed_date_time','stored_date_time','number_of_tubes']
        widgets = {
            "collected_date_time": forms.DateTimeInput,
            "processed_date_time": forms.DateTimeInput
        }

class KitSentForm(forms.Form):
    kit_sent_date = forms.DateField(initial=timezone.now())