import datetime

from django import forms
from django.forms import TextInput
import logging
from biospecimen.models import CaregiverBiospecimen,Status,Declined,ReceivedWSU,ShippedMSU,ReceivedMSU,Incentive,Component,BLOOD_DICT_FORM,BLOOD_DICT,BLOOD_DICT_DISPLAY,NotCollected
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


logging.basicConfig(level=logging.CRITICAL)

CHOICES = [('C','Complete')]
IN_PERSON_REMOTE = [('I','In Person'),('R','Remote')]
COLLECTED_NOT_COLLECTED = [('C', 'Collected'), ('N', 'Not Collected')]
COLLECTED_NOT_COLLECTED_NO_CONSENT = [('C', 'Collected'), ('N', 'Not Collected'), ('O', 'No Consent')]
KIT_SENT_NOT_COLLECTED_DECLINED = [('K', 'Kit Sent'), ('N', 'Not Collected'), ('X', 'Declined')]
KIT_SENT_NOT_COLLECTED = [('K','Kit Sent'),('N','Not Collected')]
SHIPPED_CHOICE = [('W','Shipped to WSU'),('E','Shipped to Echo')]
SHIPPED_CHOICE_ECHO = [('E','Shipped to Echo')]
COURIERS = [('F','FedEx'),('P','USPS'),('U','UPS'),('D','DHL')]
PROCESSED_ALIQUOTED_OFF_SITE = [('N','Not Applicable'),('R','Refigerated'),('T','Room Temperature')]
YES_NO=[('Y','Yes'),('N','No')]


def check_component_tubes(component_values, form_data,cleaned_data,chain_of_custody):
    for blood_item in form_data.items():
        for component in component_values:
            try:
                logging.debug(f"blood is {blood_item[0]}")
                logging.debug(f"is data true or false is {blood_item[1]}")
                logging.debug(f"component is data is {BLOOD_DICT[component.get_component_type_display()]}")
                if blood_item[1] and (blood_item[0] == BLOOD_DICT[component.get_component_type_display()]):
                    logging.debug("made it into tube check")
                    number_of_tubes = cleaned_data[blood_item[0] + "_number_of_tubes"]
                    logging.debug(
                        f"blood logging {blood_item[0]} form data: {number_of_tubes} component number of tubes {component.number_of_tubes}")
                    if number_of_tubes != component.number_of_tubes:
                        raise ValidationError(
                            _("%(component)s number of tubes entered %(form_tubes)s does not match number of %(component)s %(chain_of_custody)s tubes: %(component_tube)s"),
                            code="ValidationError",
                            params={"component": BLOOD_DICT_DISPLAY[blood_item[0]],
                                    "component_tube": component.number_of_tubes, "form_tubes": number_of_tubes,"chain_of_custody":chain_of_custody})
            except KeyError:
                pass

class ShippedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    shipping_number = forms.CharField()
    quantity = forms.IntegerField()
    shipped_date_time = forms.DateTimeField(initial=timezone.now())
    logged_date_time = forms.DateTimeField()
    courier = forms.CharField()

class StoredBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select,choices=CHOICES)
    stored_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    storage_location = forms.CharField()
    quantity = forms.IntegerField()
    logged_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class ProcessedBiospecimenForm(forms.Form):
    outcome_fk = forms.ChoiceField(widget=forms.Select,choices=CHOICES)
    collected_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    processed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    quantity = forms.IntegerField()
    logged_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))

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
        fields = ['collection_fk','status_fk']
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
        fields = ['incentive_date',]

    def __init__(self, *args, **kwargs):
        super(IncentiveForm, self).__init__(*args, **kwargs)
        self.fields['incentive_date'].widget = TextInput(attrs={
            'class': 'datepicker'})

class CollectedBiospecimenForm(forms.Form):
    collected_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    processed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    stored_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    placed_in_formalin = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    received_date = forms.DateField(widget=forms.TextInput(attrs={'class': "datepicker"}))
    number_of_tubes = forms.IntegerField()
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)

class CollectedBiospecimenPlacentaForm(forms.Form):
    collected_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    processed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    placed_in_formalin = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))

    class Meta:
        fields = ['collected_date_time','processed_date_time','placed_in_formalin']
        widgets = {
            "collected_date_time": forms.DateTimeInput,
            "processed_date_time": forms.DateTimeInput
        }

class CollectedBiospecimenUrineForm(forms.Form):
    eat_drink_datetime = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the last time the participant ate or drank anything other than plain water?')
    eat_drink_text_field = forms.CharField(max_length=255, required=False,label='List everything that was consumed the last time the particpiant ate or drank anything:')
    collected_date_time = forms.DateTimeField( widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    notes_and_deviations = forms.CharField(max_length=255,required=False)

    class Meta:
        fields = ['collected_date_time','processed_date_time','stored_date_time','number_of_tubes','notes_and_deviations']
        widgets = {
            "collected_date_time": forms.DateTimeInput,
            "processed_date_time": forms.DateTimeInput
        }

class ProcessedFormUrine(forms.Form):
    processed_aliquoted_off_site = forms.ChoiceField(widget=forms.Select, choices=PROCESSED_ALIQUOTED_OFF_SITE,label='If processed and aliquoted off site, under what conditions were the tubes transported to the processing site?')
    processed_aliquoted_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the specimen received at the processing site?')
    total_volume_of_urine_in_collection_cup = forms.IntegerField(label='What is the total volume of urine in the collection cup?',max_value=150,min_value=0)
    precipate_bottom_of_container = forms.BooleanField(label='Are there precipitate(s) at the bottom of the collection container?')
    refigerated_prior_to_processing = forms.BooleanField(label='Was the collection cup placed at refrigerated temperature prior to processing?')
    refigerated_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collected cup placed at refrigerated temperature?')
    refigerated_removed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collection cup removed from refrigerated temperature for processing?')
    all_18_collected = forms.ChoiceField(label='Were all seven of the 1.8 mL urine aliquots collected? (orange cap)',choices=YES_NO)
    partial_aliquot_18ml_1 = forms.BooleanField(required=False,label='Partial Aliquot #1')
    partial_aliquot_18ml_1_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #1 Amount')
    partial_aliquot_18ml_2 = forms.BooleanField(required=False,label='Partial Aliquot #2')
    partial_aliquot_18ml_2_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #2 Amount')
    partial_aliquot_18ml_3 = forms.BooleanField(required=False,label='Partial Aliquot #3')
    partial_aliquot_18ml_3_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #3 Amount')
    partial_aliquot_18ml_4 = forms.BooleanField(required=False,label='Partial Aliquot #4')
    partial_aliquot_18ml_4_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #4 Amount')
    partial_aliquot_18ml_5 = forms.BooleanField(required=False,label='Partial Aliquot #5')
    partial_aliquot_18ml_5_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #5 Amount')
    partial_aliquot_18ml_6 = forms.BooleanField(required=False,label='Partial Aliquot #6')
    partial_aliquot_18ml_6_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #6 Amount')
    partial_aliquot_18ml_7 = forms.BooleanField(required=False,label='Partial Aliquot #7')
    partial_aliquot_18ml_7_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #7 Amount')
    all_7_collected = forms.ChoiceField(label='Were all four of the 7 mL urine aliquots collected? (orange cap)', choices=YES_NO)
    partial_aliquot_7ml_1 = forms.BooleanField(required=False)
    partial_aliquot_7ml_1_amount = forms.FloatField(max_value=7.0,min_value=0)
    partial_aliquot_7ml_2 = forms.BooleanField(required=False)
    partial_aliquot_7ml_2_amount = forms.FloatField(max_value=7.0,min_value=0)
    partial_aliquot_7ml_3 = forms.BooleanField(required=False)
    partial_aliquot_7ml_3_amount = forms.FloatField(max_value=7.0,min_value=0)
    partial_aliquot_7ml_4 = forms.BooleanField(required=False)
    partial_aliquot_7ml_4_amount = forms.FloatField(max_value=7.0,min_value=0)
    notes_and_deviations = forms.CharField(max_length=255,required=False)


class InitialBioForm(forms.Form):
    collected_not_collected = forms.ChoiceField(widget=forms.Select, choices=COLLECTED_NOT_COLLECTED)

class InitialBioFormPostNatal(forms.Form):
    collected_not_collected_kit_sent = forms.ChoiceField(widget=forms.Select, choices=KIT_SENT_NOT_COLLECTED_DECLINED)

class InitialBioFormPeriNatal(forms.Form):
    collected_not_collected_no_consent = forms.ChoiceField(widget=forms.Select, choices=COLLECTED_NOT_COLLECTED_NO_CONSENT)

class InitialBioFormChildTooth(forms.Form):
    collected_not_collected_kit_sent = forms.ChoiceField(widget=forms.Select, choices=KIT_SENT_NOT_COLLECTED_DECLINED)

class ShippedChoiceForm(forms.Form):
    shipped_to_wsu_or_echo = forms.ChoiceField(widget=forms.Select,choices=SHIPPED_CHOICE)

class ShippedChoiceEchoForm(forms.Form):
    shipped_to_wsu_or_echo = forms.ChoiceField(widget=forms.Select,choices=SHIPPED_CHOICE_ECHO)

class ShippedtoWSUForm(forms.Form):
    shipped_date_and_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    tracking_number = forms.CharField()
    number_of_tubes = forms.IntegerField()
    logged_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    courier = forms.ChoiceField(widget=forms.Select,choices=COURIERS)

class ShippedtoWSUFormBlood(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    tracking_number = forms.CharField()
    logged_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    courier = forms.ChoiceField(widget=forms.Select,choices=COURIERS)
    whole_blood = forms.BooleanField(required=False)
    whole_blood_number_of_tubes = forms.IntegerField(required=False)
    plasma = forms.BooleanField(required=False)
    plasma_number_of_tubes = forms.IntegerField(required=False)
    buffy_coat = forms.BooleanField(required=False)
    buffy_coat_number_of_tubes = forms.IntegerField(required=False)
    red_blood_cells = forms.BooleanField(required=False)
    red_blood_cells_number_of_tubes = forms.IntegerField(required=False)
    serum = forms.BooleanField(required=False)
    serum_number_of_tubes = forms.IntegerField(required=False)

    # https://stackoverflow.com/questions/24251141/pass-data-to-django-forms-field-clean-method
    def __init__(self, *args,**kwargs):
        self.caregiver_bio = kwargs.pop('caregiver_bio')
        super(ShippedtoWSUFormBlood,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super().clean()
        component_values = Component.objects.filter(caregiver_biospecimen_fk=self.caregiver_bio)
        logging.debug(f"component values{component_values}")
        test_data = {k: cleaned_data[k] for k in BLOOD_DICT.values()}
        check_component_tubes(component_values=component_values,form_data=test_data,cleaned_data=cleaned_data,chain_of_custody='collected')

class ReceivedatWSUBloodForm(forms.Form):
    received_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    whole_blood = forms.BooleanField(required=False)
    whole_blood_number_of_tubes = forms.IntegerField(required=False)
    plasma = forms.BooleanField(required=False)
    plasma_number_of_tubes = forms.IntegerField(required=False)
    buffy_coat = forms.BooleanField(required=False)
    buffy_coat_number_of_tubes = forms.IntegerField(required=False)
    red_blood_cells = forms.BooleanField(required=False)
    red_blood_cells_number_of_tubes = forms.IntegerField(required=False)
    serum = forms.BooleanField(required=False)
    serum_number_of_tubes = forms.IntegerField(required=False)

    def __init__(self, *args,**kwargs):
        self.caregiver_bio = kwargs.pop('caregiver_bio')
        super(ReceivedatWSUBloodForm,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super().clean()
        component_values = Component.objects.filter(caregiver_biospecimen_fk=self.caregiver_bio)
        logging.debug(f"component values{component_values}")
        test_data = {k: cleaned_data[k] for k in BLOOD_DICT.values()}
        check_component_tubes(component_values=component_values,form_data=test_data,cleaned_data=cleaned_data,chain_of_custody='shipped to wsu')


class ShippedtoEchoBloodForm(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

    def __init__(self, *args,**kwargs):
        self.caregiver_bio = kwargs.pop('caregiver_bio')
        super(ShippedtoEchoBloodForm,self).__init__(*args,**kwargs)


class ShippedtoWSUFormPlacenta(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    tracking_number = forms.CharField()
    courier = forms.ChoiceField(widget=forms.Select,choices=COURIERS)

class ShippedtoWSUFormChild(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class ReceivedatWSUFormChild(forms.Form):
    receive_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class ShippedtoEchoForm(forms.Form):
    shipped_date_and_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class CollectedBloodForm(forms.Form):
    collected_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    processed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    stored_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    whole_blood = forms.BooleanField(required=False)
    whole_blood_number_of_tubes = forms.IntegerField(required=False)
    plasma = forms.BooleanField(required=False)
    plasma_number_of_tubes = forms.IntegerField(required=False)
    buffy_coat = forms.BooleanField(required=False)
    buffy_coat_number_of_tubes = forms.IntegerField(required=False)
    red_blood_cells = forms.BooleanField(required=False)
    red_blood_cells_number_of_tubes = forms.IntegerField(required=False)
    serum = forms.BooleanField(required=False)
    serum_number_of_tubes = forms.IntegerField(required=False)

    class Meta:
        fields = ['collected_date_time','processed_date_time','stored_date_time','number_of_tubes']
        widgets = {
            "collected_date_time": forms.DateTimeInput,
            "processed_date_time": forms.DateTimeInput
        }

class KitSentForm(forms.Form):
    kit_sent_date = forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))
    echo_biospecimen_id = forms.CharField()

class CollectedChildUrineStoolForm(forms.Form):
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)
    date_received = forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))
    number_of_tubes = forms.IntegerField()

class CollectedChildBloodSpotForm(forms.Form):
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)
    date_received = forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))
    number_of_cards = forms.IntegerField()

class CollectedBiospecimenHairSalivaForm(forms.Form):
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)
    date_collected =forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))

class CollectedChildBloodSpotHairFormOneYear(forms.Form):
    in_person_remote = forms.ChoiceField(widget=forms.Select,choices=IN_PERSON_REMOTE)
    date_received =forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))

class CollectedChildToothForm(forms.Form):
    date_collected =forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))

class ReceivedatWSUForm(forms.Form):
    received_date_time = forms.DateTimeField(initial=timezone.now(),
                                             widget=forms.TextInput(attrs={'class': "datetimepicker"}))
    number_of_tubes = forms.IntegerField(required=False)

    def __str__(self):
        return f"{self.received_date_time}"


class DeclinedForm(forms.Form):
    declined_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

    # def __init__(self, *args, **kwargs):
    #     super(DeclinedForm, self).__init__(*args, **kwargs)
    #     self.fields['declined_date'].widget = TextInput(attrs={
    #         'class': 'datepicker'})

class NotCollectedForm(forms.Form):
    CHOICES = [
        ('1', 'Refused'),
        ('2', 'Other'),
    ]
    refused_or_other = forms.ChoiceField(widget=forms.RadioSelect, choices=NotCollected.RefusedOrOther.choices,label='')
    other_specify = forms.CharField(widget=forms.TextInput(attrs={'id': 'other_specify_input'}),required=False)


class ShippedtoMSUForm(forms.ModelForm):
    class Meta:
        model = ShippedMSU
        fields = ['shipped_date_time']

    def __init__(self, *args, **kwargs):
        super(ShippedtoMSUForm, self).__init__(*args, **kwargs)
        self.fields['shipped_date_time'].widget = TextInput(attrs={
            'class': 'datetimepicker'})

class ReceivedatMSUForm(forms.ModelForm):
    class Meta:
        model = ReceivedMSU
        fields = ['received_date_time']

    def __init__(self, *args, **kwargs):
        super(ReceivedatMSUForm, self).__init__(*args, **kwargs)
        self.fields['received_date_time'].widget = TextInput(attrs={
            'class': 'datetimepicker'})