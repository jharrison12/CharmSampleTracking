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
PROCESSED_ALIQUOTED_OFF_SITE = [('N','Not Applicable'),('R','refrigerated'),('T','Room Temperature')]
BLOOD_PROCESSED_ALIQUOTED = [('N','Not Applicable'),('R','Refrigerated'),('T','Room Temperature'),('D','Dry Ice')]
YES_NO=[(True,'Yes'),(False,'No')]
PARTIAL_COMPLETE = [('C','Complete'),('P','Partial'),('N','Not Collected')]
HEMOLYSIS = [('N','None'),('M','Mild'),('O','Moderate'),('S','Severe')]


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
    processed_aliquoted_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the specimen received at the processing site?',required=False)
    total_volume_of_urine_in_collection_cup = forms.IntegerField(label='What is the total volume of urine in the collection cup?',max_value=150,min_value=0)
    precipate_bottom_of_container = forms.BooleanField(label='Are there precipitate(s) at the bottom of the collection container?',required=False)
    refrigerated_prior_to_processing = forms.BooleanField(label='Was the collection cup placed at refrigerated temperature prior to processing?',required=False)
    refrigerated_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collected cup placed at refrigerated temperature?',required=False)
    refrigerated_removed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collection cup removed from refrigerated temperature for processing?',required=False)
    all_18_collected = forms.ChoiceField(label='Were all seven of the 1.8 mL urine aliquots collected? (orange cap)',choices=YES_NO)
    partial_aliquot_18ml_1 = forms.BooleanField(required=False,label='Partial Aliquot #1')
    partial_aliquot_18ml_1_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #1 Amount',required=False)
    partial_aliquot_18ml_2 = forms.BooleanField(required=False,label='Partial Aliquot #2')
    partial_aliquot_18ml_2_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #2 Amount',required=False)
    partial_aliquot_18ml_3 = forms.BooleanField(required=False,label='Partial Aliquot #3')
    partial_aliquot_18ml_3_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #3 Amount',required=False)
    partial_aliquot_18ml_4 = forms.BooleanField(required=False,label='Partial Aliquot #4')
    partial_aliquot_18ml_4_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #4 Amount',required=False)
    partial_aliquot_18ml_5 = forms.BooleanField(required=False,label='Partial Aliquot #5')
    partial_aliquot_18ml_5_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #5 Amount',required=False)
    partial_aliquot_18ml_6 = forms.BooleanField(required=False,label='Partial Aliquot #6')
    partial_aliquot_18ml_6_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #6 Amount',required=False)
    partial_aliquot_18ml_7 = forms.BooleanField(required=False,label='Partial Aliquot #7')
    partial_aliquot_18ml_7_amount = forms.FloatField(max_value=1.8,min_value=0,label='Partial Aliquot #7 Amount',required=False)
    all_7_collected = forms.ChoiceField(label='Were all four of the 7 mL urine aliquots collected? (orange cap)', choices=YES_NO)
    partial_aliquot_7ml_1 = forms.BooleanField(required=False,label='Partial Aliquot #1')
    partial_aliquot_7ml_1_amount = forms.FloatField(max_value=7.0,min_value=0,label='Partial Aliquot #1 Amount',required=False)
    partial_aliquot_7ml_2 = forms.BooleanField(required=False,label='Partial Aliquot #2')
    partial_aliquot_7ml_2_amount = forms.FloatField(max_value=7.0,min_value=0,label='Partial Aliquot #2 Amount',required=False)
    partial_aliquot_7ml_3 = forms.BooleanField(required=False,label='Partial Aliquot #3')
    partial_aliquot_7ml_3_amount = forms.FloatField(max_value=7.0,min_value=0,label='Partial Aliquot #3 Amount',required=False)
    partial_aliquot_7ml_4 = forms.BooleanField(required=False,label='Partial Aliquot #4')
    partial_aliquot_7ml_4_amount = forms.FloatField(max_value=7.0,min_value=0,label='Partial Aliquot #4 Amount',required=False)
    notes_and_deviations = forms.CharField(max_length=255,required=False)

class FrozenFormUrine(forms.Form):
    freezer_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time cryovials were placed in the freezer:',required=False)
    number_of_tubes =forms.IntegerField(label='Total number of tubes',max_value=11,min_value=0)
    notes_and_deviations = forms.CharField(max_length=255, required=False)

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
    other_water_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the last time the participant ate or drank anything other than plain water?')
    collected_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time Collected')
    tube_1 = forms.ChoiceField(widget=forms.Select,choices=PARTIAL_COMPLETE, label='Tube #1 - Serum')
    tube_1_estimated_volume = forms.DecimalField(required=False)
    tube_1_hemolysis = forms.ChoiceField(widget=forms.Select,choices=HEMOLYSIS)
    tube_2 = forms.ChoiceField(widget=forms.Select,choices=PARTIAL_COMPLETE,label='Tube #2 - EDTA')
    tube_2_estimated_volume = forms.DecimalField(required=False)
    tube_2_hemolysis = forms.ChoiceField(widget=forms.Select,choices=HEMOLYSIS)
    tube_3 = forms.ChoiceField(widget=forms.Select,choices=PARTIAL_COMPLETE,label='Tube #3 - EDTA')
    tube_3_estimated_volume = forms.DecimalField(required=False)
    tube_3_hemolysis = forms.ChoiceField(widget=forms.Select,choices=HEMOLYSIS)
    notes = forms.CharField(max_length=255,required=False)

class ProcessedBloodForm(forms.Form):
    processed_aliquoted_off_site = forms.ChoiceField(widget=forms.Select,choices=BLOOD_PROCESSED_ALIQUOTED,label='If processed and aliquoted off site, under what conditions were the tubes transported to the processing site?')
    specimen_received_date_time =forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='If anything other than Not Applicable: When was the specimen received at the processing site?')
    edta_purple_tube_refrigerated_prior_to_centrifuge = forms.ChoiceField(required=False,choices=YES_NO,
                                                                          label='Were the purple EDTA tubes placed at refrigerated temperature prior to centrifuging?',
                                                                          initial=False)
    edta_purple_refrigerated_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),required=False,label='If Yes, date and time EDTA tubes were placed at refrigerated temperature prior to centrifuging')
    edta_purple_refrigerated_removed_date_time =forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),required=False,label='If Yes, date and time EDTA tubes were removed from refrigerated temperature for centrifuging')
    whole_blood_blue_cap_collected = forms.ChoiceField(required=False,choices=YES_NO,label='Were both Whole Blood aliquots collected? (blue cap)')
    whole_blood_blue_cap_partial_aliquot_number_1_collected = forms.BooleanField(required=False)
    whole_blood_blue_cap_partial_aliquot_number_1_amount = forms.IntegerField(required=False)
    whole_blood_blue_cap_partial_aliquot_number_2_collected = forms.BooleanField(required=False)
    whole_blood_blue_cap_partial_aliquot_number_2_amount = forms.IntegerField(required=False,label='Whole Blood aliquot #2 (blue cap) amount:')
    blood_spot_card_completed = forms.ChoiceField(required=False,choices=YES_NO,label='Was the blood spot card filled completely?')
    blood_spot_card_number_of_complete_spots = forms.IntegerField(required=False,label='Number of complete blood spots')
    blood_spot_card_number_of_dots_smaller_than_dotted_circle = forms.IntegerField(required=False,label='Number of blood spots smaller than dotted circle')
    blood_spot_card_number_of_dotted_circle_missing_blood_spot = forms.IntegerField(required=False,label='Number of dotted circles missing a blood spot')
    vacutainer_centrifuge_start_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Vacutainer centrifuge start time:')
    vacutainer_centrifuge_end_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Vacutainer centrifuge end time:')
    plasma_purple_cap_200_microliter_all_collected = forms.ChoiceField(required=False, choices=YES_NO, label='Were all seven 200 uL plasma aliquots collected? (purple cap)')
    plasma_purple_cap_200_microliter_number_collected = forms.IntegerField(required=False,label='How many (200 uL plasma aliquots) were collected?')
    plasma_purple_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label='Were all three of the 1 mL plasma aliquots collected? (purple cap)')
    plasma_purple_cap_1_ml_partial_aliquot_number_1_collected = forms.BooleanField(required=False)
    plasma_purple_cap_1_ml_partial_aliquot_number_1_amount = forms.IntegerField(required=False)
    plasma_purple_cap_1_ml_partial_aliquot_number_2_collected = forms.BooleanField(required=False)
    plasma_purple_cap_1_ml_partial_aliquot_number_2_amount = forms.IntegerField(required=False)
    plasma_purple_cap_1_ml_partial_aliquot_number_3_collected = forms.BooleanField(required=False)
    plasma_purple_cap_1_ml_partial_aliquot_number_3_amount = forms.IntegerField(required=False)
    buffy_coat_green_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label='Were both Buffy Coat aliquots collected? (green cap)?')
    buffy_coat_green_cap_1_ml_partial_aliquot_number_1_collected = forms.BooleanField(required=False)
    buffy_coat_green_cap_1_ml_partial_aliquot_number_1_amount = forms.IntegerField(required=False)
    buffy_coat_green_cap_1_ml_partial_aliquot_number_2_collected = forms.BooleanField(required=False)
    buffy_coat_green_cap_1_ml_partial_aliquot_number_2_amount = forms.IntegerField(required=False)
    red_blood_cells_yellow_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label='Were both Red Blood Cell aliquots collected? (yellow cap)')
    red_blood_cells_yellow_cap_1_ml_partial_aliquot_number_1_collected = forms.BooleanField(required=False)
    red_blood_cells_yellow_cap_1_ml_partial_aliquot_number_1_amount = forms.IntegerField(required=False)
    red_blood_cells_yellow_cap_1_ml_partial_aliquot_number_2_collected = forms.BooleanField(required=False)
    red_blood_cells_yellow_cap_1_ml_partial_aliquot_number_2_amount = forms.IntegerField(required=False)
    serum_red_cap_200_microl_all_collected = forms.ChoiceField(required=False,choices=YES_NO)
    serum_red_cap_200_microl_number_collected = forms.IntegerField(required=False)
    serum_red_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO)
    serum_red_cap_1_ml_partial_aliquot_number_1_collected = forms.BooleanField(required=False)
    serum_red_cap_1_ml_partial_aliquot_number_1_amount = forms.IntegerField(required=False)
    serum_red_cap_1_ml_partial_aliquot_number_2_collected = forms.BooleanField(required=False)
    serum_red_cap_1_ml_partial_aliquot_number_2_amount = forms.IntegerField(required=False)
    serum_red_cap_1_mlpartial_aliquot_number_1_collected = forms.BooleanField(required=False)
    serum_red_cap_1_mlpartial_aliquot_number_1_amount = forms.IntegerField(required=False)
    serum_red_cap_1_mlpartial_aliquot_number_2_collected = forms.BooleanField(required=False)
    serum_red_cap_1_mlpartial_aliquot_number_2_amount = forms.IntegerField(required=False)
    notes = forms.CharField(max_length=255,required=False)

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

    def __str__(self):
        return f"{self.received_date_time}"


class DeclinedForm(forms.Form):
    declined_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

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