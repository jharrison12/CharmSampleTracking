import logging

from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Collection, Collected, NotCollected, NoConsent, ShippedWSU, ShippedECHO, \
    KitSent, Incentive, Declined, ReceivedWSU, ShippedMSU,ReceivedMSU,Project,Caregiver,Trimester,Child,Component
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,CollectedBiospecimenHairSalivaForm,ShippedChoiceEchoForm,InitialBioFormPostNatal,KitSentForm,\
ReceivedatWSUForm,InitialBioFormPeriNatal,CollectedBiospecimenPlacentaForm,ShippedtoWSUFormPlacenta,ShippedtoMSUForm,ReceivedatMSUForm
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import random

logging.basicConfig(level=logging.CRITICAL)

blood_dict = {'Whole Blood':'whole_blood',
              'Serum':'serum',
              'Plasma':'plasma',
              'Red Blood Cells':'red_blood_cells',
              'Buffy Coat':'buffy_coat'}

blood_dict_form = {'whole_blood':'W',
                   'serum':'S',
                   'plasma':'P',
                   'red_blood_cells':'R',
                   'buffy_coat':'F',
                   }


BLOOD_TYPES = ["S","P","D","W","F","R","B"]
URINE = "U"
HAIR_SALIVA = ["H","L"]
PERINATAL = ["C","X"]


def check_for_object_or_return_none(object_name,filter,parameter):
    try:
        return object_name.objects.get(filter=parameter)
    except object_name.DoesNotExist:
        return None

def create_or_update_component_values(caregiver_bio,logged_in_user,form_data,project='ECHO2'):
        logging.critical(f"What is caregiver_bio {caregiver_bio}\n")
        project_object = Project.objects.get(project_name=project)
        try:
            components = Component.objects.filter(caregiver_biospecimen_fk=caregiver_bio)
            form_components = {k: form_data[k] for k in (blood_dict_form.keys())}
            for component in form_components:
                blood_collection_component = components.get(component_type=blood_dict_form[component])
                blood_collection_component.number_of_tubes = form_data[f"{component}_number_of_tubes"]
                blood_collection_component.save()
                logging.critical(f"did blood collection component work {blood_collection_component}")
            logging.critical(f"components is {components} form components is {form_components} from data is {form_data}")
        except Status.DoesNotExist:
            new_status = Status()
            new_collected = Collected()
            biospecimen_object = CaregiverBiospecimen.objects.get(collection_fk__collection_type=collection_type,
                                                                  caregiver_fk=caregiver_object,
                                                                  trimester_fk__trimester=trimester_text,
                                                                  project_fk=project_object)
            new_status.collected_fk = new_collected
            new_collected.collected_date_time = form_data.cleaned_data['collected_date_time']
            new_collected.stored_date_time = form_data.cleaned_data['stored_date_time']
            new_collected.processed_date_time = form_data.cleaned_data['processed_date_time']
            new_collected.number_of_tubes = form_data.cleaned_data['number_of_tubes']
            new_collected.logged_by = logged_in_user
            biospecimen_object.status_fk = new_status
            new_collected.save()
            new_status.save()
            biospecimen_object.save()
            logging.debug(f"Everything created and saved {biospecimen_object}")


def update_shipped_wsu(caregiver_bio_pk,bound_form,user_logged_in):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status_bio = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    logging.debug(f"did update shipped wsu function for {caregiver_bio} find status {status_bio} ")
    try:
        shipped_to_wsu = ShippedWSU.objects.get(status=status_bio)
        logging.debug(f"shipped to wsu found {shipped_to_wsu} status_bio:{status_bio}")
    except ShippedWSU.DoesNotExist:
        logging.debug(f"Shipped to wsu not found")
        shipped_to_wsu = ShippedWSU()
        status_bio.shipped_wsu_fk = shipped_to_wsu
        logging.debug(f"shipped to wsu created status_bio: {status_bio} shipped to wsu {shipped_to_wsu}")
    shipped_to_wsu.shipped_date_time = bound_form.cleaned_data['shipped_date_and_time']
    shipped_to_wsu.tracking_number = bound_form.cleaned_data['tracking_number']
    shipped_to_wsu.number_of_tubes = bound_form.cleaned_data['number_of_tubes']
    shipped_to_wsu.courier = bound_form.cleaned_data['courier']
    shipped_to_wsu.logged_date_time = bound_form.cleaned_data['logged_date_time']
    shipped_to_wsu.shipped_by = user_logged_in
    received_object = ReceivedWSU.objects.create()
    status_bio.received_wsu_fk = received_object
    status_bio.received_wsu_fk.save()
    shipped_to_wsu.save()
    status_bio.save()
    status_bio.save()
    caregiver_bio.save()
    logging.debug(f"shipped to wsu function complete {shipped_to_wsu} status: {status_bio}\n")

def update_received_wsu(caregiver_bio_pk,data,user_logged_in):
    logging.debug(data)
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status_bio = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    try:
        received_at_wsu = ReceivedWSU.objects.get(status__caregiverbiospecimen=caregiver_bio)
        finished_form = ReceivedatWSUForm(data=data, prefix='received_at_wsu_form')
        if finished_form.is_valid():
            received_at_wsu.received_date_time = finished_form.cleaned_data['received_date_time']
            logging.debug(f"form is valid {finished_form.is_valid()}  form errors {finished_form.errors} {finished_form.cleaned_data}")
            received_at_wsu.save()
            finished_form.save()
            caregiver_bio.save()
            logging.debug(f"received at wsu found {received_at_wsu} status_bio:{status_bio} is received datetime saved {received_at_wsu.received_date_time}")
    except ReceivedWSU.DoesNotExist:
        logging.debug(f"received at wsu doesn't exist")
        received_at_wsu = ReceivedWSU.objects.create()
        finished_form = ReceivedatWSUForm(data=data,prefix='received_at_wsu_form')
        if finished_form.is_valid():
            caregiver_bio.status_fk.received_wsu_fk = received_at_wsu
            caregiver_bio.status_fk.received_wsu_fk.received_date_time = finished_form.cleaned_data['received_date_time']
            received_at_wsu.save()
            caregiver_bio.status_fk.received_wsu_fk.save()
            caregiver_bio.status_fk.save()
            caregiver_bio.save()

def update_shipped_echo(caregiver_bio_pk, bound_form):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status_bio = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    try:
        shipped_to_echo = ShippedECHO.objects.get(status=status_bio)
    except ShippedECHO.DoesNotExist:
        shipped_to_echo = ShippedECHO()
        status_bio.shipped_echo_fk = shipped_to_echo
    shipped_to_echo.shipped_date_time = bound_form.cleaned_data['shipped_date_and_time']
    shipped_to_echo.save()
    status_bio.save()
    caregiver_bio.save()

def create_or_update_incentive(caregiver_bio_pk, bound_form):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    try:
        incentive_item = Incentive.objects.get(caregiverbiospecimen=caregiver_bio)
    except Incentive.DoesNotExist:
        incentive_item = Incentive()
        caregiver_bio.incentive_fk = incentive_item
    logging.debug(f"{incentive_item}")
    logging.debug(f"{bound_form.cleaned_data}")
    incentive_item.incentive_date = bound_form.cleaned_data['incentive_date']
    incentive_item.save()
    caregiver_bio.save()


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
def caregiver_biospecimen(request,caregiver_charm_id):
    #TODO: Fix this so you're iterating over one queryset and not 15
    caregiver = get_object_or_404(Caregiver,charm_project_identifier=caregiver_charm_id)
    caregiver_collection_query = CaregiverBiospecimen.objects.values('collection_fk__collection_type_fk__collection_type')
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
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    logging.debug(f"collection type {collection_type} "
                     f"{HAIR_SALIVA}"
                     f"collection type in hair saliva? {collection_type in HAIR_SALIVA}"
                     f"collection type in hair saliva? {collection_type in HAIR_SALIVA}")
                     # f"{collection_type.objects.filter(id=HAIR_SALIVA.id).exists()}")
    if caregiver_bio.status_fk==None and collection_type not in HAIR_SALIVA and collection_type not in PERINATAL:
        logging.debug(f"made it to INCORRECT initial bio form")
        initial_bio_form = InitialBioForm(prefix="initial_form")
    elif caregiver_bio.status_fk==None and collection_type in PERINATAL:
        initial_bio_form = InitialBioFormPeriNatal(prefix="initial_form")
    elif caregiver_bio.status_fk==None and collection_type in HAIR_SALIVA:
        logging.debug(f"made it to correct initial bio form")
        initial_bio_form = InitialBioFormPostNatal(prefix="initial_form")
    else:
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
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method=="POST" and collection_type not in HAIR_SALIVA and collection_type not in PERINATAL:
        form = InitialBioForm(data=request.POST, prefix='initial_form')
        logging.critical(f"{form.is_valid()} {form} {form.errors} collection type {collection_type} "
                         f"\n\nperinatal {PERINATAL}"
                         f"\n\n is collection_type in PERINATAL {collection_type in PERINATAL}")
        if form.is_valid():
            new_status = Status()
            caregiver_bio.status_fk = new_status
            new_status.save()
            caregiver_bio.save()
            if form.cleaned_data['collected_not_collected']=='C':
                new_collected = Collected.objects.create(logged_by=request.user)
                new_status.collected_fk = new_collected
            elif form.cleaned_data['collected_not_collected']=='N':
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected']=='X':
                new_declined = Declined.objects.create()
                new_status.declined_fk = new_declined
            new_status.save()
            caregiver_bio.save()
            if collection_type in BLOOD_TYPES:
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
            new_status = Status()
            caregiver_bio.status_fk = new_status
            new_status.save()
            caregiver_bio.save()
            if form.cleaned_data['collected_not_collected_kit_sent'] == 'X':
                new_declined = Declined.objects.create()
                new_status.declined_fk = new_declined
            elif form.cleaned_data['collected_not_collected_kit_sent'] == 'N':
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected_kit_sent'] == 'K':
                new_kit_sent = KitSent.objects.create()
                new_status.kit_sent_fk = new_kit_sent
            new_status.save()
            caregiver_bio.save()
            return redirect("biospecimen:caregiver_biospecimen_entry_hair_saliva", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError

    elif request.method == "POST" and collection_type in PERINATAL:
        form = InitialBioFormPeriNatal(data=request.POST, prefix='initial_form')
        logging.debug(f"is form valid {form} {form.is_valid()}")
        if form.is_valid():
            new_status = Status()
            caregiver_bio.status_fk = new_status
            new_status.save()
            caregiver_bio.save()
            if form.cleaned_data['collected_not_collected_no_consent'] == 'O':
                new_no_consent = NoConsent.objects.create()
                new_status.no_consent_fk = new_no_consent
            elif form.cleaned_data['collected_not_collected_no_consent'] == 'N':
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected_no_consent'] == 'C':
                new_collected = Collected.objects.create()
                new_status.collected_fk = new_collected
            new_status.save()
            caregiver_bio.save()
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
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    kit_sent_item = KitSent.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    kit_sent_form = None
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
                                                                                                  'kit_sent_form':kit_sent_form
                                                                                                  })
@login_required()
def caregiver_biospecimen_kit_sent_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    if request.method == "POST" and collection_type in HAIR_SALIVA:
        form = KitSentForm(data=request.POST, prefix='kit_sent_form')
        if form.is_valid():
            kit_sent_data = KitSent.objects.get(status__caregiverbiospecimen=caregiver_bio)
            kit_sent_data.kit_sent_date = form.cleaned_data['kit_sent_date']
            caregiver_bio.biospecimen_id = form.cleaned_data['echo_biospecimen_id']
            kit_sent_data.save()
            collected_item = Collected.objects.create()
            caregiver_bio.status_fk.collected_fk = collected_item
            caregiver_bio.status_fk.collected_fk.save()
            caregiver_bio.status_fk.save()
            caregiver_bio.save()

        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
    else:
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)


@login_required
def caregiver_biospecimen_entry(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_wsu_item = ReceivedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_msu_item = ShippedMSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_msu_item = ReceivedMSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    incentive_form = None
    received_at_wsu_form = None
    shipped_to_msu_form = None
    received_msu_form = None
    logging.debug(f"Collection type is {collection_type}")
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
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=True):
            logging.debug(f"in shipped to wsu if statement")
            shipped_wsu_form = ShippedtoWSUFormPlacenta(prefix="shipped_to_wsu_form")
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=False) and not received_at_wsu_item:
            logging.debug(f"made it to received at wsu form")
            received_at_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
        if received_at_wsu_item.exists() and not shipped_to_echo_item:
            logging.debug(f"in shipped to echo if statement")
            shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    elif collection_type==URINE:
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
            collected_form = CollectedBiospecimenUrineForm(prefix='urine_form')
        if collected_item.exists() and caregiver_bio.incentive_fk and not caregiver_bio.incentive_fk.incentive_date:
            incentive_form = IncentiveForm(prefix='incentive_form')
        if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and caregiver_bio.incentive_fk.incentive_date and\
            not shipped_to_wsu_item and not shipped_to_echo_item :
            shipped_choice = ShippedChoiceForm(prefix='shipped_choice_form')
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=True):
            shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
        if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=False) and not received_at_wsu_item:
            logging.debug(f"made it to received at wsu form")
            received_at_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
        if shipped_to_echo_item.exists() and shipped_to_echo_item.filter(shipped_date_time__isnull=True):
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
                                                                                                  })

@login_required
def caregiver_biospecimen_entry_blood(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_wsu_item = ReceivedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    incentive_form = None
    received_wsu_form = None
    logging.debug(f"Caregiver bio is {caregiver_bio}")
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True).exists():
        logging.debug(f"Does collected_item exist? {collected_item.exists()}\n\n"
                         f"Is collected date time null {collected_item.filter(collected_date_time__isnull=True).exists()}\n")
        logging.debug(f"in Collected form if statement")
        collected_form = CollectedBloodForm(prefix='blood_form')
        logging.debug(blood_dict.get(collection_type))
        # disable whatever check box you used to pull the data
        logging.critical(f"collection type {collection_type}")
        if collection_type!=Collection.CollectionType.BLOOD:
            collected_form.fields[str(blood_dict.get(collection_type))].initial = True
            collected_form.fields[str(blood_dict.get(collection_type))].disabled = True
        # collected_form.fields[str(blood_dict.get(collection_type))].widget.attrs['readonly'] = True
    else:
        logging.debug(f"Collected form is none")
        collected_form = None
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and not caregiver_bio.incentive_fk:
        incentive_form = IncentiveForm(prefix='incentive_form')
    elif collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and caregiver_bio.incentive_fk.incentive_date \
            and not (caregiver_bio.status_fk.shipped_wsu_fk or caregiver_bio.status_fk.shipped_echo_fk):
        logging.debug(f"Made it to shipped choice")
        shipped_choice = ShippedChoiceForm(prefix='shipped_choice_form')
    elif shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=True):
        logging.debug(f"in shipped to wsu if statement")
        shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
    elif received_at_wsu_item.exists() and received_at_wsu_item.filter(received_date_time__isnull=True):
        received_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
    elif shipped_to_echo_item.exists() and shipped_to_echo_item.filter(shipped_date_time__isnull=True):
        logging.debug(f"in shipped to echo if statement")
        shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry_blood.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                        'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                        'caregiver_bio': caregiver_bio,
                                                                                                        'collected_form': collected_form,
                                                                                                        'collection_type': collection_type,
                                                                                                        'shipped_choice_form': shipped_choice,
                                                                                                        'shipped_wsu_form': shipped_wsu_form,
                                                                                                        'shipped_echo_form': shipped_echo_form,
                                                                                                        'incentive_form':incentive_form,
                                                                                                        'received_wsu_form':received_wsu_form
                                                                                                        })

@login_required
def caregiver_biospecimen_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    logging.debug(f"collection type {collection_type} caregiver {caregiver_bio.caregiver_fk.charm_project_identifier}"
                     f"")
    if request.method=="POST":
        if collection_type==URINE:
            form = CollectedBiospecimenUrineForm(data=request.POST, prefix='urine_form')
            if form.is_valid():
                collected_urine = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                collected_urine.collected_date_time = form.cleaned_data['collected_date_time']
                collected_urine.processed_date_time = form.cleaned_data['processed_date_time']
                collected_urine.stored_date_time = form.cleaned_data['stored_date_time']
                collected_urine.number_of_tubes = form.cleaned_data['number_of_tubes']
                collected_urine.logged_by = request.user
                collected_urine.save()
                incentive = Incentive.objects.create()
                caregiver_bio.incentive_fk = incentive
                caregiver_bio.incentive_fk.save()
                caregiver_bio.save()
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in HAIR_SALIVA:
            form = CollectedBiospecimenHairSalivaForm(data=request.POST, prefix='hair_saliva_form')
            if form.is_valid():
                hair_or_saliva = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                hair_or_saliva.collected_date_time = form.cleaned_data['date_collected']
                hair_or_saliva.in_person_remote = form.cleaned_data['in_person_remote']
                hair_or_saliva.logged_by = request.user
                hair_or_saliva.save()
                caregiver_bio.save()
                incentive = Incentive.objects.create()
                caregiver_bio.incentive_fk = incentive
                caregiver_bio.incentive_fk.save()
                caregiver_bio.save()
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in PERINATAL:
            form = CollectedBiospecimenPlacentaForm(data=request.POST, prefix='placenta_form')
            if form.is_valid():
                placenta = Collected.objects.get(status__caregiverbiospecimen=caregiver_bio)
                placenta.collected_date_time = form.cleaned_data['collected_date_time']
                placenta.processed_date_time = form.cleaned_data['processed_date_time']
                placenta.placed_in_formalin_date_time = form.cleaned_data['placed_in_formalin']
                placenta.logged_by = request.user
                placenta.save()
                caregiver_bio.save()
                incentive = Incentive.objects.create()
                caregiver_bio.incentive_fk = incentive
                caregiver_bio.incentive_fk.save()
                caregiver_bio.save()
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in BLOOD_TYPES:
            logging.debug(f"in the blood if statement")
            form = CollectedBloodForm(data=request.POST,prefix='blood_form')
            logging.debug(f"is form valid {form.is_valid()} \n\nform errors {form.errors} \n\nform {form.data} \n\nrequest.post{request.POST}")
            if form.is_valid():
                #I'm disabling field that references the collection type of the page
                #disabled fields are not passed through the post request, so you have to do it manually :/
                form.cleaned_data[str(blood_dict.get(collection_type))] = True
                logging.critical(f"Did form cleaned data update work {form.cleaned_data} ")

                create_or_update_component_values(caregiver_bio=caregiver_bio,
                                                  logged_in_user=request.user,
                                                  form_data=form.cleaned_data)
                # create_or_update_blood_values(true_or_false=form.cleaned_data['blood'],
                #                                       collection_type=Collection.CollectionType.BLOOD,
                #                                       caregiver_object=caregiver,
                #                                       trimester_text=caregiver_bio.trimester_fk,
                #                                       form_data=form,
                #                                       caregiver_bio_primary=caregiver_bio_pk,
                #                                       logged_in_user=request.user)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    else:
        raise AssertionError

@login_required()
def caregiver_biospecimen_incentive_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if request.method=="POST":
        if collection_type in HAIR_SALIVA or collection_type==URINE:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                incentive_item =Incentive.objects.get(caregiverbiospecimen=caregiver_bio)
                incentive_item.incentive_date = form.cleaned_data['incentive_date']
                incentive_item.logged_by = request.user
                incentive_item.save()
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
                incentive_item.incentive_date = form.cleaned_data['incentive_date']
                incentive_item.logged_by = request.user
                shipped_to_wsu = ShippedWSU.objects.create()
                caregiver_bio.status_fk.shipped_wsu_fk = shipped_to_wsu
                caregiver_bio.status_fk.save()
                incentive_item.save()
                caregiver_bio.save()
            else:
                form.errors
            return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in BLOOD_TYPES:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                caregiver_bloods = return_caregiver_bloods(caregiver_bio)
                for item in caregiver_bloods:
                    logging.debug(f"Blood item is {item}")
                    create_or_update_incentive(item.pk, form)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError

@login_required
def caregiver_shipped_choice_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
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
                logging.debug(f'Shipped to wsu saved')
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'E':
                shipped_to_echo = ShippedECHO.objects.create()
                status.shipped_echo_fk = shipped_to_echo
                status.save()
                logging.debug(f'Shipped to echo saved')
            caregiver_bio.save()
            if collection_type in BLOOD_TYPES:
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
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In wsu post")
    if request.method == "POST":
        if collection_type in BLOOD_TYPES:
            caregiver_bloods = return_caregiver_bloods(caregiver_bio)
            form = ShippedtoWSUForm(data=request.POST, prefix='shipped_to_wsu_form')
            logging.debug(f"form is valid {form.is_valid()}  form errors {form.errors}")
            logging.debug(f"caregiver bloods {caregiver_bloods}")
            if form.is_valid():
                for item in caregiver_bloods:
                    logging.debug(f"updating shipped wsu {item.pk}")
                    update_shipped_wsu(caregiver_bio_pk=item.pk,bound_form=form,user_logged_in=request.user)
                return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type in PERINATAL:
            logging.debug(f"post is {request.POST}")
            form = ShippedtoWSUFormPlacenta(data=request.POST, prefix='shipped_to_wsu_form')
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_wsu_fk.shipped_date_time = form.cleaned_data['shipped_date_and_time']
                shipped_wsu_fk.tracking_number = form.cleaned_data['tracking_number']
                shipped_wsu_fk.courier = form.cleaned_data['courier']
                shipped_wsu_fk.shipped_by = request.user
                shipped_wsu_fk.save()
                logging.debug(f"shipped wsu saved")
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            logging.debug(f"post is {request.POST}")
            form = ShippedtoWSUForm(data=request.POST, prefix='shipped_to_wsu_form')
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_wsu_fk.shipped_date_time = form.cleaned_data['shipped_date_and_time']
                shipped_wsu_fk.tracking_number = form.cleaned_data['tracking_number']
                shipped_wsu_fk.number_of_tubes = form.cleaned_data['number_of_tubes']
                shipped_wsu_fk.logged_date_time = form.cleaned_data['logged_date_time']
                shipped_wsu_fk.courier = form.cleaned_data['courier']
                shipped_wsu_fk.save()
                logging.debug(f"shipped wsu saved")
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_received_wsu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In received wsu post")
    if request.method == "POST":
        if collection_type in BLOOD_TYPES:
            caregiver_bloods = return_caregiver_bloods(caregiver_bio)
            logging.debug(f"care giver bloods {caregiver_bloods}")
            for item in caregiver_bloods:
                logging.debug(f"updating recieved wsu {item.pk}")
                update_received_wsu(caregiver_bio_pk=item.pk, data=request.POST, user_logged_in=request.user)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
        elif collection_type==URINE or collection_type in PERINATAL:
            update_received_wsu(caregiver_bio_pk=caregiver_bio_pk,data=request.POST,user_logged_in=request.user)
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
    return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_shipped_msu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_to_msu_item = ShippedMSU.objects.create(status=status)
    logging.debug(f"In msu post")
    if request.method == "POST":
        if collection_type in HAIR_SALIVA:
            logging.debug(f"post is {request.POST}")
            form = ShippedtoMSUForm(data=request.POST, prefix='shipped_to_msu_form')
            logging.debug(f"is shipped to msu form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_to_msu_item.shipped_date_time = form.cleaned_data['shipped_date_time']
                status.shipped_msu_fk = shipped_to_msu_item
                shipped_to_msu_item.save()
                status.save()
                caregiver_bio.save()
                logging.debug(f"shipped msu saved")
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_received_at_msu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    received_msu_item = ReceivedMSU.objects.create(status=status)
    logging.debug(f"In received msu post")
    if request.method == "POST":
        if collection_type in HAIR_SALIVA:
            form = ReceivedatMSUForm(data=request.POST,prefix='received_at_msu_form')
            logging.debug(f"is received to msu form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                received_msu_item.received_date_time = form.cleaned_data['received_date_time']
                status.received_msu_fk = received_msu_item
                received_msu_item.save()
                status.save()
                caregiver_bio.save()
                logging.debug(f"shipped msu saved")
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                    caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_shipped_echo_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = Collection.objects.get(caregiverbiospecimen=caregiver_bio).collection_type
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_echo_fk = ShippedECHO.objects.create(status=status)
    logging.debug(f"In echo post")
    if request.method == "POST":
        if collection_type in BLOOD_TYPES:
            caregiver_bloods = return_caregiver_bloods(caregiver_bio)
            logging.debug(f"post is {request.POST}")
            form = ShippedtoEchoForm(data=request.POST, prefix='shipped_to_echo_form')
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                for item in caregiver_bloods:
                    update_shipped_echo(caregiver_bio_pk=item.pk,bound_form=form)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)
        else:
            logging.debug(f"post is {request.POST}")
            form = ShippedtoEchoForm(data=request.POST, prefix='shipped_to_echo_form')
            logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
            if form.is_valid():
                shipped_echo_fk.shipped_date_time = form.cleaned_data['shipped_date_and_time']
                shipped_echo_fk.save()
                status.shipped_echo_fk = shipped_echo_fk
                status.save()
                logging.debug(f"shipped echo saved")
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                    caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError