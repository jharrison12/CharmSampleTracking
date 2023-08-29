from django import forms
from dataview.models import CaregiverBiospecimen

class CaregiverBiospecimenForm(forms.models.ModelForm):

    class Meta:
        model = CaregiverBiospecimen
        fields = ('collection_fk','status_fk','incentive_fk','biospecimen_date',)
