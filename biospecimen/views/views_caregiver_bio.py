import logging

from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Collection, Collected, NotCollected, \
    NoConsent, ShippedWSU, ShippedECHO, \
    KitSent, Incentive, Declined, ReceivedWSU, ShippedMSU, ReceivedMSU, Project, Caregiver, PregnancyTrimester, Child, \
    Component, URINE, BLOOD_DICT_FORM, BLOOD_DICT, ComponentError, \
    ProcessedUrine, UrineAliquot, Frozen, BloodTube, ProcessedBlood, BloodAliquot, BloodSpotCard
from biospecimen.forms import CaregiverBiospecimenForm, IncentiveForm, CollectedBiospecimenUrineForm, InitialBioForm, \
    ShippedChoiceForm, ShippedtoWSUForm, \
    ShippedtoEchoForm, CollectedBloodForm, CollectedBiospecimenHairSalivaForm, ShippedChoiceEchoForm, \
    InitialBioFormPostNatal, KitSentForm, \
    ReceivedatWSUForm, InitialBioFormPeriNatal, CollectedBiospecimenPlacentaForm, ShippedtoWSUFormPlacenta, \
    ShippedtoMSUForm, ReceivedatMSUForm, ShippedtoWSUFormBlood, \
    ReceivedatWSUBloodForm, ShippedtoEchoBloodForm, ShippedtoEchoForm, DeclinedForm, NotCollectedForm, \
    ProcessedFormUrine, FrozenFormUrine, ProcessedBloodForm, FrozenFormBlood
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages

logging.basicConfig(level=logging.CRITICAL)


BLOOD = ["B"]
BLOOD_TYPES = ["S","P","D","W","F","R"]
# URINE = "U"
HAIR_SALIVA = ["H","L"]
PERINATAL = ["C","X"]



def check_for_object_or_return_none(object_name,filter,parameter):
    try:
        return object_name.objects.get(filter=parameter)
    except object_name.DoesNotExist:
        return None

def return_caregiver_bloods(caregiver_bio,collected_fk=None,shipped_wsu_fk=None,received_wsu_fk=None,shipped_echo_fk=None):
    logging.debug(f"in caregiver bloods collected")
    if collected_fk:
        return Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio,number_of_tubes__isnull=False,collected_fk=collected_fk)
    elif shipped_wsu_fk:
        return Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio, number_of_tubes__isnull=False,
                                        shipped_wsu_fk=shipped_wsu_fk)
    elif received_wsu_fk:
        return Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio, number_of_tubes__isnull=False,
                                        received_wsu_fk=received_wsu_fk)
    elif shipped_echo_fk:
        return Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio, number_of_tubes__isnull=False,
                                        shipped_echo_fk=shipped_echo_fk)

def return_blood_tubes(caregiver_bio):
    return BloodTube.objects.filter(caregiver_biospecimen_fk=caregiver_bio)

def create_or_update_component_values(caregiver_bio,logged_in_user,form_data,collected_fk=None,shipped_wsu_fk=None, received_wsu_fk=None,shipped_to_echo_fk=None,project='ECHO2'):
        logging.debug(f"What is caregiver_bio {caregiver_bio}\n")
        logging.debug(f"What is form data {form_data}\n")
        try:
            components = Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio)
            form_components = {k: form_data[k] for k in (BLOOD_DICT_FORM.keys())}
            for component in form_components:
                if component:
                    blood_collection_component = components.get(component_type=BLOOD_DICT_FORM[component])
                    blood_collection_component.number_of_tubes = form_data[f"{component}_number_of_tubes"]
                    if collected_fk:
                        blood_collection_component.collected_fk = collected_fk
                    elif shipped_wsu_fk:
                        blood_collection_component.shipped_wsu_fk = shipped_wsu_fk
                    elif received_wsu_fk:
                        blood_collection_component.received_wsu_fk =received_wsu_fk
                    elif shipped_to_echo_fk:
                        blood_collection_component.shipped_echo_fk = shipped_to_echo_fk
                    blood_collection_component.save()
                    caregiver_bio.save()
                    logging.debug(f"did blood collection component work {blood_collection_component}")
            logging.debug(f"components is {components}\n form components is {form_components}\n form data is {form_data}")
        except Status.DoesNotExist:
            raise ValueError

def update_shipped_wsu(caregiver_bio_pk,bound_form,request,collection_type=None):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status_bio = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    logging.debug(f"did update shipped wsu function for {caregiver_bio} find status {status_bio} ")
    try:
        shipped_to_wsu = ShippedWSU.objects.get(status=status_bio)
        logging.debug(f"shipped to wsu found {shipped_to_wsu} status_bio:{status_bio}")
    except ShippedWSU.DoesNotExist:
        logging.debug(f"Shipped to wsu not found")
        shipped_to_wsu = ShippedWSU.objects.create()
        logging.debug(f"shipped to wsu created status_bio: {status_bio} shipped to wsu {shipped_to_wsu}")
    shipped_to_wsu.save_shipped_wsu(form=bound_form,request=request,caregiver_bio=caregiver_bio,collection_type=collection_type)
    logging.debug(f"shipped to wsu function complete {shipped_to_wsu} status: {status_bio}\n")

def update_received_wsu(caregiver_bio_pk,data,bound_form,user_logged_in,request):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        received_at_wsu = ReceivedWSU.objects.get(status__caregiverbiospecimen=caregiver_bio)
        if bound_form.is_valid():
            received_at_wsu.save_received_wsu(caregiver_bio=caregiver_bio,request=request,form=bound_form)
    except ReceivedWSU.DoesNotExist:
        received_at_wsu = ReceivedWSU.objects.create()
        #finished_form = ReceivedatWSUForm(data=data,prefix='received_at_wsu_form')
        #why did you bind the form a second time?
        if bound_form.is_valid():
            received_at_wsu.save_received_wsu(caregiver_bio=caregiver_bio,request=request,form=bound_form)

def compare_form_component(component_values,form):
    for component in component_values:
        logging.debug(
            f"{component} {component.number_of_tubes} {component.component_type} {component.get_component_type_display()} form {form.cleaned_data}")
        for value in BLOOD_DICT.keys():
            logging.debug(f"blood dict key {value} blood dict return value {BLOOD_DICT[value]}")
            logging.debug(f"{form.cleaned_data[BLOOD_DICT[value]]}")
            logging.debug(f"{BLOOD_DICT.get(component.get_component_type_display())}")
            try:
                if form.cleaned_data[f"{BLOOD_DICT[value]}"] and\
                    (BLOOD_DICT[value] == BLOOD_DICT.get(component.get_component_type_display())):
                    logging.debug(f"In form cleaned data check")
                    if form.cleaned_data[f"{BLOOD_DICT.get(component.get_component_type_display())}_number_of_tubes"] != component.number_of_tubes:
                        raise ComponentError
            except KeyError:
                pass

#################################################
# Views
##################################################
@login_required
def home_page(request):
    return render(request=request,template_name='biospecimen/home.html')

@login_required
def biospecimen_entry(request):
    list_of_echo_2_bio = CaregiverBiospecimen.objects.filter(project_fk__project_name='ECHO2')
    return render(request, template_name='biospecimen/biospecimen_entry.html', context={'list_of_biospecimens':list_of_echo_2_bio})

@login_required
def charm_identifiers(request):
    if request.user.is_staff:
        list_of_charm_ids = Caregiver.objects.all()
    else:
        location = request.user.recruitment_location
        list_of_charm_ids = Caregiver.objects.filter(recruitment_location=location)
    return render(request,template_name='biospecimen/charm_identifiers.html',context={'list_of_charm_ids':list_of_charm_ids})

@login_required
def list_of_bio_ids(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    try:
        caregiver.check_recruitment(request=request,caregiver=caregiver)
    except PermissionError:
        logging.error('in permission error')
        return redirect('biospecimen:error_page')
    list_of_biospecimen_ids = CaregiverBiospecimen.objects.filter(caregiver_fk=caregiver)
    trimester_2_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk=caregiver,trimester_fk__trimester=PregnancyTrimester.TrimesterChoices.SECOND)
    trimester_3_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk=caregiver,trimester_fk__trimester=PregnancyTrimester.TrimesterChoices.THIRD)
    perinatal_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk=caregiver,perinatal_fk__isnull=False)
    postnatal_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk=caregiver,age_category_fk__isnull=False)
    return render(request, template_name='biospecimen/list_of_mother_bio_ids.html', context={'list_of_biospecimen_ids':list_of_biospecimen_ids,
                                                                                             'trimester_2_biospecimens':trimester_2_biospecimens,
                                                                                             'trimester_3_biospecimens':trimester_3_biospecimens,
                                                                                             'perinatal_biospecimens':perinatal_biospecimens,
                                                                                             'postnatal_biospecimens':postnatal_biospecimens,
                                                                                            'caregiver':caregiver})

@login_required
def caregiver_biospecimen(request,caregiver_charm_id):
    #TODO: What is this view used for??????
    #TODO: Fix this so you're iterating over one queryset and not 15
    caregiver = get_object_or_404(Caregiver,charm_project_identifier=caregiver_charm_id)
    caregiver_collection_query = CaregiverBiospecimen.objects.values('collection_fk__collection_type')
    caregiver_collections = list(set(val for dic in caregiver_collection_query for val in dic.values()))
    caregiver_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request, template_name='biospecimen/caregiver_biospecimen.html', context={'caregiver':caregiver,
                                                                                            'caregiver_collections':caregiver_collections,
                                                                                            'caregiver_biospecimens':caregiver_biospecimens})

@login_required
def child_biospecimen_page(request,child_charm_id):
    child = get_object_or_404(Child,charm_project_identifier=child_charm_id)
    child_collection_query = ChildBiospecimen.objects.values('collection_fk__collection_type_fk__collection_type')
    child_collections = list(set(val for dic in child_collection_query for val in dic.values()))
    child_biospecimens = ChildBiospecimen.objects.filter(child_fk__charm_project_identifier=child_charm_id)
    return render(request, template_name='biospecimen/child_biospecimen.html', context={'child':child,
                                                                                   'child_collections':child_collections,
                                                                                   'child_biospecimens':child_biospecimens})


@login_required
def caregiver_biospecimen_initial(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        logging.error('in permission error')
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if caregiver_bio.status_fk==None:
        if collection_type not in HAIR_SALIVA and collection_type not in PERINATAL:
            initial_bio_form = InitialBioForm(prefix="initial_form")
        elif collection_type in PERINATAL:
            initial_bio_form = InitialBioFormPeriNatal(prefix="initial_form")
        elif collection_type in HAIR_SALIVA:
            logging.debug(f"made it to correct initial bio form")
            initial_bio_form = InitialBioFormPostNatal(prefix="initial_form")
        else:
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        if collection_type in BLOOD:
            return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type:
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    return render(request, template_name='biospecimen/caregiver_biospecimen_initial.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'initial_bio_form':initial_bio_form,
                                                                                                  'collection_type': collection_type
                                                                                                    })



@login_required
def caregiver_biospecimen_initial_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method=="POST" and collection_type not in HAIR_SALIVA and collection_type not in PERINATAL:
        form = InitialBioForm(data=request.POST, prefix='initial_form')
        if form.is_valid():
            new_status = Status.objects.create()
            initial_status = new_status.save_initial_form(form=form,caregiver_bio=caregiver_bio,request=request)
            logging.critical(f"initial status is {initial_status}")
            logging.critical(f" is instance {isinstance(initial_status,NotCollected)}")
            if initial_status=='N':
                logging.critical(f"Found not collected")
                return redirect("biospecimen:caregiver_biospecimen_not_collected", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
            elif collection_type in BLOOD:
                return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
            else:
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    elif request.method=="POST" and collection_type in HAIR_SALIVA:
        form = InitialBioFormPostNatal(data=request.POST, prefix='initial_form')
        logging.debug(f"is form valid {form} {form.is_valid()}")
        if form.is_valid():
            new_status = Status.objects.create()
            new_status.save_initial_form(form=form,caregiver_bio=caregiver_bio,request=request)
            return redirect("biospecimen:caregiver_biospecimen_entry_hair_saliva", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError

    elif request.method == "POST" and collection_type in PERINATAL:
        form = InitialBioFormPeriNatal(data=request.POST, prefix='initial_form')
        logging.debug(f"is form valid {form} {form.is_valid()}")
        if form.is_valid():
            new_status = Status.objects.create()
            new_status.save_initial_form(form=form,caregiver_bio=caregiver_bio,request=request)
            return redirect("biospecimen:caregiver_biospecimen_entry",
                            caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError

    else:
        return redirect("biospecimen:caregiver_biospecimen_initial",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)



@login_required
def caregiver_biospecimen_entry_hair_saliva(request, caregiver_charm_id, caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    kit_sent_item = KitSent.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    declined_item = Declined.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    kit_sent_form = None
    declined_form = None
    if declined_item.exists() and declined_item.filter(declined_date__isnull=True):
        declined_form = DeclinedForm(prefix='declined_form')
    if kit_sent_item.exists() and collection_type in HAIR_SALIVA:
        kit_sent_form = KitSentForm(prefix="kit_sent_form")
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'collected_form':collected_form,
                                                                                                  'collection_type': collection_type,
                                                                                                  'shipped_choice_form': shipped_choice,
                                                                                                  'shipped_wsu_form': shipped_wsu_form,
                                                                                                  'shipped_echo_form':shipped_echo_form,
                                                                                                  'kit_sent_form':kit_sent_form,
                                                                                                  'declined_form':declined_form,
                                                                                                  'declined_item':declined_item
                                                                                                  })
@login_required
def caregiver_biospecimen_kit_sent_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method == "POST" and collection_type in HAIR_SALIVA:
        form = KitSentForm(data=request.POST, prefix='kit_sent_form')
        if form.is_valid():
            KitSent.objects.get(status__caregiverbiospecimen=caregiver_bio).save_form(form=form,request=request)
            caregiver_bio.biospecimen_id = form.cleaned_data['echo_biospecimen_id']
            Collected.objects.create().create_collected_and_set_status_fk(caregiver_bio=caregiver_bio)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
    else:
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_entry(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    incentive_item = Incentive.objects.filter(caregiverbiospecimen=caregiver_bio)
    processed_item = ProcessedUrine.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    frozen_item = Frozen.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_wsu_item = ReceivedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_msu_item = ShippedMSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_msu_item = ReceivedMSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    not_collected_item = NotCollected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    urine_aliquot_18ml_items = UrineAliquot.objects.filter(processed_fk__status__caregiverbiospecimen=caregiver_bio,aliquot_vial_size=UrineAliquot.VialAmount.EIGHTEEN_ML)
    urine_aliquot_7ml_items = UrineAliquot.objects.filter(processed_fk__status__caregiverbiospecimen=caregiver_bio,aliquot_vial_size=UrineAliquot.VialAmount.SEVEN_ML)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    incentive_form = None
    received_at_wsu_form = None
    shipped_to_msu_form = None
    received_msu_form = None
    not_collected_form = None
    processed_form = None
    frozen_form = None
    if collection_type in HAIR_SALIVA:
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
            collected_form = CollectedBiospecimenHairSalivaForm(prefix='hair_saliva_form')
        if collected_item.exists() and caregiver_bio.incentive_fk and not caregiver_bio.incentive_fk.incentive_date:
            incentive_form = IncentiveForm(prefix='incentive_form')
        if collected_item.exists() and collected_item.filter(
                collected_date_time__isnull=False) and caregiver_bio.incentive_fk.incentive_date and not shipped_to_msu_item:
            shipped_to_msu_form = ShippedtoMSUForm(prefix='shipped_to_msu_form')
        if shipped_to_msu_item.exists() and shipped_to_msu_item.filter(shipped_date_time__isnull=False) and not received_at_msu_item:
            logging.debug(f"in shipped to msu if statement")
            received_msu_form = ReceivedatMSUForm(prefix="received_at_msu_form")
        if received_at_msu_item.exists() and received_at_msu_item.filter(received_date_time__isnull=False) and not shipped_to_echo_item:
            logging.debug(f"in shipped to echo if statement")
            shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    elif collection_type in PERINATAL:
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
            collected_form = CollectedBiospecimenPlacentaForm(prefix='placenta_form')
        if collected_item.exists() and caregiver_bio.incentive_fk and not caregiver_bio.incentive_fk.incentive_date:
            incentive_form = IncentiveForm(prefix='incentive_form')
        if incentive_item.exists() and incentive_item.filter(incentive_date__isnull=False) and not shipped_to_wsu_item.exists():
            logging.debug(f"in shipped to wsu if statement")
            shipped_wsu_form = ShippedtoWSUFormPlacenta(prefix="shipped_to_wsu_form")
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=False) and not received_at_wsu_item:
            logging.debug(f"made it to received at wsu form")
            received_at_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
        if received_at_wsu_item.exists() and not shipped_to_echo_item:
            logging.debug(f"in shipped to echo if statement")
            shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    elif collection_type==URINE:
        logging.debug(f'{ not processed_item}')
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
            collected_form = CollectedBiospecimenUrineForm(prefix='urine_form')
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and not processed_item:
            processed_form = ProcessedFormUrine(prefix='processed_form')
        if processed_item.exists() and not frozen_item:
            frozen_form = FrozenFormUrine(prefix='frozen_form')
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and frozen_item and not shipped_to_wsu_item:
            shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=False) and not received_at_wsu_item:
            logging.debug(f"made it to received at wsu form")
            received_at_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
        if received_at_wsu_item.exists() and received_at_wsu_item.filter(received_date_time__isnull=False)\
                and (not shipped_to_echo_item.exists() or shipped_to_echo_item.filter(shipped_date_time__isnull=True)):
            logging.debug(f"in shipped to echo if statement")
            shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'collected_form':collected_form,
                                                                                                  'collection_type': collection_type,
                                                                                                  'shipped_choice_form': shipped_choice,
                                                                                                  'shipped_wsu_form': shipped_wsu_form,
                                                                                                  'shipped_echo_form':shipped_echo_form,
                                                                                                  'incentive_form': incentive_form,
                                                                                                  'received_at_wsu_form':received_at_wsu_form,
                                                                                                  'shipped_to_msu_form':shipped_to_msu_form,
                                                                                                  'received_msu_form':received_msu_form,
                                                                                                  'not_collected_form':not_collected_form,
                                                                                                  'not_collected_item': not_collected_item,
                                                                                                  'processed_item':processed_item,
                                                                                                  'processed_form':processed_form,
                                                                                                  'urine_aliquot_18ml_items': urine_aliquot_18ml_items,
                                                                                                  'urine_aliquot_7ml_items': urine_aliquot_7ml_items,
                                                                                                  'frozen_item':frozen_item,
                                                                                                  'frozen_form':frozen_form
                                                                                                  })

@login_required
def caregiver_biospecimen_entry_blood(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    logging.critical(f'caregiver bio is {caregiver_bio} pk {caregiver_bio.pk}')
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    caregiver_bloods_collected = None
    caregiver_bloods_shipped_wsu = None
    caregiver_bloods_received_wsu = None
    caregiver_bloods_shipped_echo = None
    if caregiver_bio.status_fk and caregiver_bio.status_fk.collected_fk:
        caregiver_bloods_collected = return_blood_tubes(caregiver_bio=caregiver_bio)
        logging.critical(f"caregiver blood tubes {caregiver_bloods_collected}")
    if caregiver_bio.status_fk and caregiver_bio.status_fk.shipped_wsu_fk:
        caregiver_bloods_shipped_wsu = return_caregiver_bloods(caregiver_bio,shipped_wsu_fk=caregiver_bio.status_fk.shipped_wsu_fk)
    if caregiver_bio.status_fk and caregiver_bio.status_fk.received_wsu_fk:
        caregiver_bloods_received_wsu = return_caregiver_bloods(caregiver_bio,received_wsu_fk=caregiver_bio.status_fk.received_wsu_fk)
    if caregiver_bio.status_fk and caregiver_bio.status_fk.shipped_echo_fk:
        caregiver_bloods_shipped_echo = return_caregiver_bloods(caregiver_bio,shipped_echo_fk=caregiver_bio.status_fk.shipped_echo_fk)
        logging.debug(f"Caregiver bloods {caregiver_bloods_shipped_echo}")
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_wsu_item = ReceivedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    not_collected_item = NotCollected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    processed_item = ProcessedBlood.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    frozen_item = Frozen.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    blood_aliquots = BloodAliquot.objects.filter(caregiver_bio_fk=caregiver_bio)
    try:
        blood_spot_card = BloodSpotCard.objects.get(caregiver_bio_fk=caregiver_bio)
    except BloodSpotCard.DoesNotExist:
        logging.critical(f"Blood spots card not found")
        blood_spot_card = None
    logging.critical(f'blood aliquots are {blood_aliquots}')
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    incentive_form = None
    received_wsu_form = None
    not_collected_form= None
    collected_form=None
    processed_form = None
    frozen_form = None
    logging.critical(f"Caregiver bio is {caregiver_bio}")
    logging.critical(f"if value for not collected blood bio is {not_collected_item.exists()} {not_collected_item.filter(refused_or_other__isnull=True).exists()}")
    if not_collected_item.exists() and not_collected_item.filter(refused_or_other__isnull=True).exists():
        logging.critical(f"made it to not collected form")
        not_collected_form = NotCollectedForm(prefix='not_collected_form')
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True).exists():
        collected_form = CollectedBloodForm(prefix='blood_form')
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and not processed_item:
            logging.critical(f"in processed form if block")
            processed_form = ProcessedBloodForm(prefix='processed_form')
    elif collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and processed_item \
            and not (caregiver_bio.status_fk.frozen_fk):
        frozen_form = FrozenFormBlood(prefix="frozen_form")
    elif collected_item.exists() and frozen_item.exists() and frozen_item.filter(freezer_placed_date_time__isnull=False) and not caregiver_bio.status_fk.shipped_wsu_fk:
        shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
    elif shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=False) and not (caregiver_bio.status_fk.received_wsu_fk):
        received_wsu_form = ReceivedatWSUBloodForm(prefix="received_at_wsu_form",caregiver_bio=caregiver_bio)
    elif received_at_wsu_item.exists() and received_at_wsu_item.filter(received_date_time__isnull=False)\
        and (not shipped_to_echo_item.exists() or shipped_to_echo_item.filter(shipped_date_time__isnull=True)):
        logging.debug(f"in shipped to echo if statement")
        shipped_echo_form = ShippedtoEchoBloodForm(prefix="shipped_to_echo_form",caregiver_bio=caregiver_bio)
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry_blood.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                        'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                        'caregiver_bio': caregiver_bio,
                                                                                                        'collected_form': collected_form,
                                                                                                        'collection_type': collection_type,
                                                                                                        'shipped_choice_form': shipped_choice,
                                                                                                        'shipped_wsu_form': shipped_wsu_form,
                                                                                                        'shipped_echo_form': shipped_echo_form,
                                                                                                        'incentive_form':incentive_form,
                                                                                                        'received_wsu_form':received_wsu_form,
                                                                                                        'caregiver_bloods_collected':caregiver_bloods_collected,
                                                                                                        'caregiver_bloods_shipped_wsu':caregiver_bloods_shipped_wsu,
                                                                                                        'caregiver_bloods_received_wsu':caregiver_bloods_received_wsu,
                                                                                                        'caregiver_bloods_shipped_echo':caregiver_bloods_shipped_echo,
                                                                                                        'not_collected_form':not_collected_form,
                                                                                                        'not_collected_item':not_collected_item,
                                                                                                        'processed_form':processed_form,
                                                                                                        'processed_item':processed_item,
                                                                                                        'blood_aliquots':blood_aliquots,
                                                                                                        'blood_spot_card':blood_spot_card,
                                                                                                        'frozen_form':frozen_form,
                                                                                                        'shipped_to_wsu_item':shipped_to_wsu_item
                                                                                                        })

@login_required
def caregiver_biospecimen_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    logging.debug(f"collection type {collection_type} caregiver {caregiver_bio.caregiver_fk.charm_project_identifier}"
                     f"")
    if request.method=="POST":
        if collection_type==URINE:
            form = CollectedBiospecimenUrineForm(data=request.POST, prefix='urine_form')
            if form.is_valid():
                logging.debug(f"Is form valie {form.is_valid()}")
                collected_urine = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                collected_urine.save_urine(form=form,request=request)
                Incentive.objects.create().save_fk(caregiver_bio=caregiver_bio)
            else:
                messages.info(request, f"{form.non_field_errors()}")
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in HAIR_SALIVA:
            form = CollectedBiospecimenHairSalivaForm(data=request.POST, prefix='hair_saliva_form')
            if form.is_valid():
                hair_or_saliva = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                hair_or_saliva.save_hair_saliva(form=form,request=request)
                Incentive.objects.create().save_fk(caregiver_bio=caregiver_bio)
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in PERINATAL:
            form = CollectedBiospecimenPlacentaForm(data=request.POST, prefix='placenta_form')
            if form.is_valid():
                placenta = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                placenta.save_placenta(form=form,request=request)
                Incentive.objects.create().save_fk(caregiver_bio=caregiver_bio)
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in BLOOD:
            form = CollectedBloodForm(data=request.POST,prefix='blood_form')
            logging.critical(f'in collection type blood post page')
            if form.is_valid():
                blood_item = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                blood_item.save_blood(form=form,request=request,caregiver_bio=caregiver_bio)
            else:
                messages.info(request, f"{form.errors}")
            return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    else:
        raise AssertionError

@login_required()
def caregiver_biospecimen_incentive_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method=="POST":
        if collection_type in HAIR_SALIVA or collection_type==URINE:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                incentive_item =Incentive.objects.get(caregiverbiospecimen=caregiver_bio)
                incentive_item.save_incentive(form,request)
                caregiver_bio.save()
            else:
                form.errors
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        if collection_type in PERINATAL:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                #create shipped wsu so logic skips shipped choice form
                #refactor this at some point
                incentive_item =Incentive.objects.get(caregiverbiospecimen=caregiver_bio)
                incentive_item.save_incentive(form,request)
            else:
                form.errors
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in BLOOD:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                incentive_item = Incentive.objects.create()
                incentive_item.save_fk(caregiver_bio=caregiver_bio)
                incentive_item.save_incentive_blood(bound_form=form,request=request)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError

@login_required
def caregiver_shipped_choice_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    if request.method=="POST":
        logging.debug(f"post is {request.POST}")
        form = ShippedChoiceForm(data=request.POST, prefix='shipped_choice_form')
        logging.debug(f"is shipped form valid {form.is_valid()}  {form.errors}")
        if form.is_valid():
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'W':
                shipped_to_wsu = ShippedWSU.objects.create(shipped_by=request.user)
                status.shipped_wsu_fk = shipped_to_wsu
                status.save()
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'E':
                shipped_to_echo = ShippedECHO.objects.create()
                status.shipped_echo_fk = shipped_to_echo
                status.save()
            caregiver_bio.save()
            if collection_type in BLOOD:
                return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
            else:
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_shipped_wsu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method == "POST":
        if collection_type in BLOOD:
            form = ShippedtoWSUFormBlood(data=request.POST, prefix='shipped_to_wsu_form')
            logging.debug(f"IN views shipped wsu post")
            if form.is_valid():
                logging.debug(f"Shipped to wsu form valid")
                update_shipped_wsu(caregiver_bio_pk=caregiver_bio.pk,bound_form=form,request=request,collection_type=collection_type)
            else:
                logging.debug(f"form errors? {form.errors}")
                messages.info(request, f"{form.non_field_errors()}")
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)

        elif collection_type in PERINATAL:
            form = ShippedtoWSUFormPlacenta(data=request.POST, prefix='shipped_to_wsu_form')
            if form.is_valid():
                shipped_wsu_item = ShippedWSU.objects.create()
                shipped_wsu_item.save_shipped_wsu(form=form,request=request,caregiver_bio=caregiver_bio)
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in URINE:
            form = ShippedtoWSUForm(data=request.POST, prefix='shipped_to_wsu_form')
            if form.is_valid():
                shipped_wsu_item = ShippedWSU.objects.create()
                shipped_wsu_item.save_shipped_wsu(form=form,request=request,caregiver_bio=caregiver_bio,collection_type='U',)
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_received_wsu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In received wsu post")
    if request.method == "POST":
        if collection_type in BLOOD:
            form = ReceivedatWSUBloodForm(data=request.POST, prefix='received_at_wsu_form',caregiver_bio=caregiver_bio)
            if form.is_valid():
                update_received_wsu(caregiver_bio_pk=caregiver_bio.pk, data=request.POST,request=request, user_logged_in=request.user,bound_form=form)
                create_or_update_component_values(caregiver_bio=caregiver_bio, logged_in_user=request.user,
                                                  form_data=form.cleaned_data,
                                                  collected_fk=None, shipped_wsu_fk=None, received_wsu_fk=caregiver_bio.status_fk.received_wsu_fk)
            else:
                logging.debug(f"form errors? {form.errors}")
                messages.info(request, f"{form.non_field_errors()}")
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type==URINE or collection_type in PERINATAL:
            form = ReceivedatWSUForm(data=request.POST, prefix='received_at_wsu_form')
            if form.is_valid():
                update_received_wsu(caregiver_bio_pk=caregiver_bio_pk,data=request.POST,request=request,user_logged_in=request.user,bound_form=form)
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
    return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_shipped_msu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method == "POST":
        if collection_type in HAIR_SALIVA:
            form = ShippedtoMSUForm(data=request.POST, prefix='shipped_to_msu_form')
            logging.debug(f"is shipped to msu form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_to_msu_item = ShippedMSU.objects.create()
                shipped_to_msu_item.save_msu_item(form=form,caregiver_bio=caregiver_bio,request=request)
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_received_at_msu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method == "POST":
        if collection_type in HAIR_SALIVA:
            form = ReceivedatMSUForm(data=request.POST,prefix='received_at_msu_form')
            logging.debug(f"is received to msu form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                received_msu_item = ReceivedMSU.objects.create()
                received_msu_item.save_received_msu_item(form=form,caregiver_bio=caregiver_bio,request=request)
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_shipped_echo_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    shipped_echo_item = ShippedECHO.objects.create()
    if request.method == "POST":
        if collection_type in BLOOD:
            form = ShippedtoEchoBloodForm(data=request.POST, prefix='shipped_to_echo_form',caregiver_bio=caregiver_bio)
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_echo_item.set_shipped_date_time_and_fk_and_save(form=form,request=request,caregiver_bio=caregiver_bio)
            else:
                logging.debug(f"form errors? {form.errors}")
                messages.info(request, f"{form.non_field_errors()}")
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
        else:
            logging.debug(f"post is {request.POST}")
            if collection_type in URINE:
                form  = ShippedtoEchoForm(data=request.POST,prefix='shipped_to_echo_form')
            else:
                form = ShippedtoEchoForm(data=request.POST, prefix='shipped_to_echo_form')
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_echo_item.set_shipped_date_time_and_fk_and_save(form=form,request=request,caregiver_bio=caregiver_bio)
                logging.debug(f"shipped echo saved")
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                    caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_declined_post(request, caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    declined_item = Declined.objects.get(status__caregiverbiospecimen=caregiver_bio)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    logging.debug(f'{declined_item}')
    if request.method=="POST":
        form = DeclinedForm(data=request.POST, prefix='declined_form')
        if form.is_valid():
            declined_item.save_declined(form=form,request=request,caregiver_bio=caregiver_bio)
    if collection_type in BLOOD:
        return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
    return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_processed_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    processed_item = ProcessedUrine.objects.create()
    logging.debug(f'in processed post for URINE')
    if request.method == "POST":
        form = ProcessedFormUrine(data=request.POST,prefix='processed_form')
        if form.is_valid():
            processed_item.save_processed(form=form,request=request,caregiver_bio=caregiver_bio)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_frozen_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    frozen_item = Frozen.objects.create()
    logging.debug(f'in processed post for URINE')
    if request.method == "POST":
        form = FrozenFormUrine(data=request.POST,prefix='frozen_form')
        if form.is_valid():
            frozen_item.save_frozen(form=form,request=request,caregiver_bio=caregiver_bio)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_frozen_blood_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    frozen_item = Frozen.objects.create()
    logging.debug(f'in processed post for URINE')
    if request.method == "POST":
        form = FrozenFormBlood(data=request.POST,prefix='frozen_form')
        if form.is_valid():
            frozen_item.save_frozen(form=form,request=request,caregiver_bio=caregiver_bio)
        return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_not_collected_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    not_collected_item = NotCollected.objects.get(status__caregiverbiospecimen=caregiver_bio)
    logging.debug(f'{not_collected_item}')
    if request.method == "POST":
        form = NotCollectedForm(data=request.POST, prefix='not_collected_form')
        if form.is_valid():
            not_collected_item.save_not_collected(form=form, request=request)
    return redirect("biospecimen:caregiver_biospecimen_not_collected", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_not_collected(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    not_collected_item = NotCollected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    logging.critical(f"does not collected item exist {not_collected_item.exists()}")
    logging.critical(f"refused or other is null {not_collected_item.filter(refused_or_other__isnull=True).exists()}")
    not_collected_form = None
    if not_collected_item.exists() and not_collected_item.filter(refused_or_other__isnull=True).exists():
        not_collected_form = NotCollectedForm(prefix='not_collected_form')
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry_base.html',
                  context={'caregiver_bio':caregiver_bio,
                            'charm_project_identifier':caregiver_charm_id,
                            'caregiver_bio_pk':caregiver_bio_pk,
                           'not_collected_form':not_collected_form,
                           'not_collected_item':not_collected_item,
                           })

@login_required
def caregiver_biospecimen_blood_processed_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        caregiver_bio.check_recruitment(request=request,caregiver_bio=caregiver_bio,caregiver_charm_id=caregiver_charm_id)
    except PermissionError:
        return redirect('biospecimen:error_page')
    processed_item = ProcessedBlood.objects.create()
    logging.critical(f'in caregiver blood post')
    if request.method == "POST":
        form = ProcessedBloodForm(data=request.POST, prefix='processed_form')
        logging.critical(f"is form valid {form.is_valid()} {form.errors}")
        if form.is_valid():
            processed_item.save_processed(form=form, request=request,caregiver_bio=caregiver_bio)
        else:
            messages.info(request, f"{form.errors}")
    return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)

def error(request):
    return render(request=request,template_name='biospecimen/error.html')
