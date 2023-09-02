from django import forms
from dataview.models import CaregiverBiospecimen
from django.core.exceptions import ValidationError



class CaregiverBiospecimenForm(forms.models.ModelForm):

    # def save(self, caregiver_charm_fk_id):
    #     self.instance.caregiver_fk = caregiver_charm_fk_id
    #     return super().save()

    def clean(self):
        cd = self.cleaned_data
        if self.non_field_errors():
            self.add_error('caregiver_fk','DERP')
        return cd

    class Meta:
        model = CaregiverBiospecimen
        fields = ['caregiver_fk','collection_fk','status_fk','incentive_fk','biospecimen_date']
        widgets = {
            "caregiver_fk": forms.HiddenInput()
        }
