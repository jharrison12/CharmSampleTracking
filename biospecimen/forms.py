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
COURIERS = [('F','FedEx'),('S','Self')]
PROCESSED_ALIQUOTED_OFF_SITE = [('N','Not Applicable'),('R','Refrigerated'),('T','Room Temperature')]
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
    eat_drink_text_field = forms.CharField(max_length=255, required=False,label='List everything that was consumed the last time the participant ate or drank anything:')
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
    precipate_bottom_of_container = forms.ChoiceField(label='Are there precipitate(s) at the bottom of the collection container?',required=False,choices=YES_NO)
    refrigerated_prior_to_processing = forms.ChoiceField(label='Was the collection cup placed at refrigerated temperature prior to processing?',required=False,choices=YES_NO,initial=False)
    refrigerated_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collected cup placed at refrigerated temperature?',required=False)
    refrigerated_removed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='When was the collection cup removed from refrigerated temperature for processing?',required=False)
    all_18_collected = forms.ChoiceField(label='Were all seven of the 1.8 mL urine aliquots collected? (orange cap)',choices=YES_NO)
    partial_aliquot_18ml_volume = forms.FloatField(required=False,label='If any aliquots were partial, what is the estimated volume of the partial aliquot?',max_value=1.8,min_value=0)
    number_of_tubes_collected_18_ml_if_some_missing = forms.IntegerField(max_value=7,min_value=1,label='If any aliquots were missing, how many were collected?',required=False)
    all_7_collected = forms.ChoiceField(label='Were all four of the 7 mL urine aliquots collected? (orange cap)', choices=YES_NO)
    partial_aliquot_7ml_volume = forms.FloatField(required=False,label='If any aliquots were partial, what is the estimated volume of the partial aliquot?',max_value=7,min_value=0)
    number_of_tubes_collected_7_ml_if_some_missing = forms.IntegerField(max_value=4,min_value=1,label='If any aliquots were missing, how many were collected?',required=False)
    notes_and_deviations = forms.CharField(max_length=255,required=False)

class FrozenFormUrine(forms.Form):
    freezer_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time cryovials were placed in the freezer:',required=False)
    number_of_tubes =forms.IntegerField(label='Total number of tubes',max_value=11,min_value=0)
    notes_and_deviations = forms.CharField(max_length=255, required=False)

class FrozenFormBlood(forms.Form):
    freezer_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time cryovials were placed in the freezer:',required=True)
    number_of_tubes =forms.IntegerField(label='Total number of tubes (not including bloodspot card)',max_value=21,min_value=0,required=True)
    blood_spot_card_placed_in_freezer = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time bloodspot card was placed in the freezer:',required=True)
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
    courier = forms.ChoiceField(widget=forms.Select,choices=COURIERS)

class ShippedtoWSUFormBlood(forms.Form):
    shipped_date_and_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Date/time shipped')
    number_of_tubes = forms.IntegerField(required=False,label='Number of tubes')
    courier = forms.ChoiceField(widget=forms.Select, choices=COURIERS,label='Courier')
    tracking_number = forms.CharField(label='Tracking number')
    #
    # whole_blood = forms.BooleanField(required=False)
    # whole_blood_number_of_tubes = forms.IntegerField(required=False)
    # plasma = forms.BooleanField(required=False)
    # plasma_number_of_tubes = forms.IntegerField(required=False)
    # buffy_coat = forms.BooleanField(required=False)
    # buffy_coat_number_of_tubes = forms.IntegerField(required=False)
    # red_blood_cells = forms.BooleanField(required=False)
    # red_blood_cells_number_of_tubes = forms.IntegerField(required=False)
    # serum = forms.BooleanField(required=False)
    # serum_number_of_tubes = forms.IntegerField(required=False)
    #
    # # https://stackoverflow.com/questions/24251141/pass-data-to-django-forms-field-clean-method
    # def __init__(self, *args,**kwargs):
    #     self.caregiver_bio = kwargs.pop('caregiver_bio')
    #     super(ShippedtoWSUFormBlood,self).__init__(*args,**kwargs)
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     component_values = Component.objects.filter(caregiver_biospecimen_fk=self.caregiver_bio)
    #     logging.debug(f"component values{component_values}")
    #     test_data = {k: cleaned_data[k] for k in BLOOD_DICT.values()}
    #     check_component_tubes(component_values=component_values,form_data=test_data,cleaned_data=cleaned_data,chain_of_custody='collected')

class ReceivedatWSUBloodForm(forms.Form):
    received_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))
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
    shipped_date_and_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}))

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
    shipped_date_and_time = forms.DateTimeField( widget=forms.TextInput(attrs={'class': "datetimepicker"}))

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
    notes_and_deviations = forms.CharField(max_length=255,required=False)

class ProcessedBloodForm(forms.Form):
    plasma_purple_cap_200_microliter_text = 'plasma 200 micro liter aliquots (purple cap)'
    whole_blood_blue_cap_text = 'whole blood aliquots (blue cap)'
    plasma_purle_cap_1_milliliter_text = '1 mL plasma aliquots (purple cap) '
    buffy_coat_green_cap_text = 'buffy coat (green cap)'
    red_blood_cells_yellow_cap_text = 'red blood cells (yellow cap)'
    serum_red_cap_200_micro_text = 'serum 200 micro liter (red cap)'
    serum_red_cap_1_ml_text = 'serum 1 ml (red cap)'

    processed_aliquoted_off_site = forms.ChoiceField(widget=forms.Select,choices=BLOOD_PROCESSED_ALIQUOTED,
                                                     label='If processed and aliquoted off site, under what conditions were the tubes transported to the processing site?')
    specimen_received_date_time =forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),
                                                     label='When was the specimen received at the processing site?',required=False)
    edta_purple_tube_refrigerated_prior_to_centrifuge = forms.ChoiceField(required=False,choices=YES_NO,
                                                                          label='Were the purple EDTA tubes placed at refrigerated temperature prior to centrifuging?',
                                                                          initial=False)
    edta_purple_refrigerated_placed_date_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),required=False,
                                                                    label='If Yes, date and time EDTA tubes were placed at refrigerated temperature prior to centrifuging')
    edta_purple_refrigerated_removed_date_time =forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),required=False,
                                                                    label='If Yes, date and time EDTA tubes were removed from refrigerated temperature for centrifuging')

    held_at_room_temperature_30_to_60_prior_to_centrifuge = forms.ChoiceField(required=False,choices=YES_NO,
                                                                          label='Was the serum (red top) tube held at room temp for 30 to 60 min prior to centrifuging',)

    whole_blood_blue_cap_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label=f'Were both {whole_blood_blue_cap_text} collected?')
    whole_blood_blue_cap_partial_aliquot_volume = forms.FloatField(required=False,max_value=1.99, min_value=0,
                                                                   label=f'If any {whole_blood_blue_cap_text} were partial, what is the estimated volume of the partial aliquot?:')
    whole_blood_blue_cap_number_collected = forms.IntegerField(required=False, label=f'If any {whole_blood_blue_cap_text} were missing, how many were collected?',max_value=1,min_value=0)

    blood_spot_card_completed = forms.ChoiceField(required=False,choices=YES_NO,label='Was the blood spot card filled completely?')
    blood_spot_card_number_of_complete_spots = forms.IntegerField(required=False,label='Number of complete blood spots',max_value=5,min_value=0)
    blood_spot_card_number_of_dots_smaller_than_dotted_circle = forms.IntegerField(required=False,label='Number of blood spots smaller than dotted circle')
    blood_spot_card_number_of_dotted_circle_missing_blood_spot = forms.IntegerField(required=False,label='Number of dotted circles missing a blood spot')

    vacutainer_centrifuge_start_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Vacutainer centrifuge start time:')
    vacutainer_centrifuge_end_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "datetimepicker"}),label='Vacutainer centrifuge end time:')

    plasma_purple_cap_200_microliter_all_collected = forms.ChoiceField(required=False, choices=YES_NO, label=f'Were all seven {plasma_purple_cap_200_microliter_text} collected?')
    plasma_purple_cap_200_microliter_number_collected = forms.IntegerField(required=False,max_value=6,min_value=0,
                                                                           label=f'If any {plasma_purple_cap_200_microliter_text} were missing, how many plasma 200 micro liter aliquots (purple cap) were collected?')

    plasma_purple_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,
                                                             label=f'Were all three of {plasma_purle_cap_1_milliliter_text} the collected?')
    plasma_purple_cap_1_ml_partial_aliquot_volume = forms.FloatField(required=False,max_value=0.99,min_value=0,
                                                                               label=f'If any {plasma_purle_cap_1_milliliter_text} were partial, what is the estimated volume of the partial aliquot?:')
    plasma_purple_cap_1_ml_number_collected = forms.IntegerField(required=False,max_value=2,min_value=0,
                                                                           label=f'If any {plasma_purle_cap_1_milliliter_text} were missing, how many {plasma_purle_cap_1_milliliter_text} were collected?')

    buffy_coat_green_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,
                                                                label=f'Were both {buffy_coat_green_cap_text} aliquots collected?')
    buffy_coat_green_cap_1_ml_number_collected = forms.IntegerField(required=False,max_value=2,min_value=0,
                                                                           label=f'If any {buffy_coat_green_cap_text} were missing, how many {buffy_coat_green_cap_text} were collected?')

    red_blood_cells_yellow_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label=f'Were both {red_blood_cells_yellow_cap_text} aliquots collected?')
    red_blood_cells_yellow_cap_1_ml_partial_aliquot_volume = forms.FloatField(required=False,max_value=1.79,min_value=0,
                                                                               label=f'If any {red_blood_cells_yellow_cap_text} were partial, what is the estimated volume of the partial aliquot?:')
    red_blood_cells_yellow_cap_1_ml_number_collected = forms.IntegerField(required=False,max_value=2,min_value=0,
                                                                           label=f'If any {red_blood_cells_yellow_cap_text} were missing, how many {red_blood_cells_yellow_cap_text} were collected?')

    serum_red_cap_200_microl_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label=f'Were all three {serum_red_cap_200_micro_text} aliquots collected?')

    serum_red_cap_200_microl_number_collected = forms.IntegerField(required=False,max_value=3,min_value=0,
                                                                          label=f'If any {serum_red_cap_200_micro_text} were missing, how many {serum_red_cap_200_micro_text} were collected?')

    serum_red_cap_1_ml_all_collected = forms.ChoiceField(required=False,choices=YES_NO,label=f'Were both {serum_red_cap_1_ml_text} aliquots collected?')
    serum_red_cap_1_ml_partial_aliquot_volume = forms.FloatField(required=False,max_value=0.99,min_value=0,
                                                                              label=f'If any {serum_red_cap_1_ml_text} were partial, what is the estimated volume of the partial aliquot?:')
    serum_red_cap_1_ml_number_collected = forms.IntegerField(required=False,max_value=2,min_value=0,
                                                                          label=f'If any {serum_red_cap_1_ml_text} were missing, how many {serum_red_cap_1_ml_text} were collected?')

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
    date_received =forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class CollectedChildToothForm(forms.Form):
    date_collected =forms.DateField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datetimepicker"}))

class ReceivedatWSUForm(forms.Form):
    received_date_time = forms.DateTimeField(
                                             widget=forms.TextInput(attrs={'class': "datetimepicker"}))

    def __str__(self):
        return f"{self.received_date_time}"


class DeclinedForm(forms.Form):
    declined_date_time = forms.DateTimeField(initial=timezone.now(),widget=forms.TextInput(attrs={'class': "datepicker"}))

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