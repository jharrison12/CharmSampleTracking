from django import forms
from dataview.models import CaregiverBiospecimen

class CaregiverBiospecimenForm(forms.models.ModelForm):

    def save(self, caregiver_charm_fk_id):
        self.instance.caregiver_fk = caregiver_charm_fk_id
        return super().save()

    class Meta:
        model = CaregiverBiospecimen
        fields = ('caregiver_fk','collection_fk','status_fk','incentive_fk','biospecimen_date',)
