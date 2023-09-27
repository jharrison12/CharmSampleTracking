import datetime

from django import forms
from dataview.models import Incentive
from biospecimen.models import CaregiverBiospecimen,Processed,Status
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS

CHOICES = [('C','Complete')]


class ProcessedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select,choices=CHOICES)
    collected_date_time = forms.DateTimeField(initial=datetime.datetime.now())
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