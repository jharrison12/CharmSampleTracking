from django import forms
from dataview.models import CaregiverBiospecimen
from django.core.exceptions import ValidationError



class CaregiverBiospecimenForm(forms.models.ModelForm):

    # def save(self, caregiver_charm_fk_id):
    #     self.instance.caregiver_fk = caregiver_charm_fk_id
    #     return super().save()

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': "You can't have a duplicate item"}
            self._update_errors(e)

    class Meta:
        model = CaregiverBiospecimen
        fields = ('caregiver_fk','collection_fk','status_fk','incentive_fk','biospecimen_date',)
