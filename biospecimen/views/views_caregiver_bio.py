import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType,Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Trimester,Project,\
    KitSent,Incentive,Declined,ReceivedWSU
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,CollectedBiospecimenHairSalivaForm,ShippedChoiceEchoForm,InitialBioFormPostNatal,KitSentForm,\
ReceivedatWSUForm
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

BLOOD_TYPES = ('Whole Blood','Serum','Plasma', 'Buffy Coat','Red Blood Cells')

HAIR_SALIVA = CollectionType.objects.filter(collection_type__in=["Hair","Saliva"])


def check_for_object_or_return_none(object_name,filter,parameter):
    try:
        return object_name.objects.get(filter=parameter)
    except object_name.DoesNotExist:
        return None

def create_or_update_blood_values(true_or_false,collection_type,caregiver_object,trimester_text,
                                  caregiver_bio_primary,form_data,logged_in_user,project='ECHO2',collection_number_object=None,):
    if true_or_false:
        logging.debug(f"What is true or false {true_or_false}\n")
        trimester = Trimester.objects.get(trimester=trimester_text)
        project_object = Project.objects.get(project_name=project)
        collection_object = Collection.objects.get(collection_type_fk__collection_type=collection_type,collection_number_fk__collection_number=collection_number_object)
        try:
            biospecimen_object = CaregiverBiospecimen.objects.get(caregiver_fk=caregiver_object,
                                             collection_fk=collection_object,
                                             trimester_fk=trimester,
                                             project_fk__project_name=project)
            status_fk = Status.objects.get(caregiverbiospecimen=biospecimen_object)
            collected_fk = Collected.objects.get(status=status_fk)

            collected_fk.collected_date_time = form_data.cleaned_data['collected_date_time']
            collected_fk.stored_date_time = form_data.cleaned_data['stored_date_time']
            collected_fk.processed_date_time = form_data.cleaned_data['processed_date_time']
            collected_fk.number_of_tubes = form_data.cleaned_data['number_of_tubes']
            collected_fk.save()
            status_fk.save()
            biospecimen_object.save()
            logging.debug(f"Collected date time in update statement {biospecimen_object.status_fk.collected_fk.collected_date_time}\n")
            logging.debug(f"Biospecimen object updated {biospecimen_object}\n")
        except CaregiverBiospecimen.DoesNotExist:
            new_status = Status()
            new_collected = Collected()
            new_biospecimen = CaregiverBiospecimen(caregiver_fk=caregiver_object,
                                                trimester_fk=trimester,
                                                project_fk=project_object,
                                                biospecimen_id=random.randrange(1000,9999),
                                                status_fk=new_status,
                                                collection_fk=collection_object
                                                )
            new_status.collected_fk = new_collected
            new_collected.collected_date_time = form_data.cleaned_data['collected_date_time']
            new_collected.stored_date_time = form_data.cleaned_data['stored_date_time']
            new_collected.processed_date_time = form_data.cleaned_data['processed_date_time']
            new_collected.number_of_tubes = form_data.cleaned_data['number_of_tubes']
            new_collected.logged_by = logged_in_user
            new_biospecimen.status_fk = new_status
            new_collected.save()
            new_status.save()
            new_biospecimen.save()
            logging.debug(f"Everything created and saved {new_biospecimen}")
    else:
        pass

def return_caregiver_bloods(caregiver_bio):
    ##TODO any bugs here?
    try:
        caregiver_bloods = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__collected_date_time=caregiver_bio.status_fk.collected_fk.collected_date_time,
                                                               status_fk__collected_fk__stored_date_time=caregiver_bio.status_fk.collected_fk.stored_date_time,
                                                               status_fk__collected_fk__number_of_tubes=caregiver_bio.status_fk.collected_fk.number_of_tubes,
                                                               collection_fk__collection_type_fk__collection_type__in=BLOOD_TYPES)
    except:
        caregiver_bloods = None
    return caregiver_bloods


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
    logging.critical(data)
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    status_bio = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    try:
        received_at_wsu = ReceivedWSU.objects.get(status__caregiverbiospecimen=caregiver_bio)
        finished_form = ReceivedatWSUForm(data=data, prefix='received_at_wsu_form')
        if finished_form.is_valid():
            received_at_wsu.received_date_time = finished_form.cleaned_data['received_date_time']
            logging.critical(f"form is valid {finished_form.is_valid()}  form errors {finished_form.errors} {finished_form.cleaned_data}")
            received_at_wsu.save()
            finished_form.save()
            caregiver_bio.save()
            logging.critical(f"received at wsu found {received_at_wsu} status_bio:{status_bio} is received datetime saved {received_at_wsu.received_date_time}")
    except ReceivedWSU.DoesNotExist:
        received_at_wsu = ReceivedWSU()
        finished_form = ReceivedatWSUForm(data=data,prefix='received_at_wsu_form')
        if finished_form.is_valid():
            caregiver_bio.status_fk.received_wsu_fk.received_date_time = finished_form
            received_at_wsu.save()
            finished_form.save()
            status_bio.received_wsu_fk = received_at_wsu
            status_bio.save()

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
    logging.critical(f"{incentive_item}")
    logging.critical(f"{bound_form.cleaned_data}")
    incentive_item.incentive_date = bound_form.cleaned_data['incentive_date']
    incentive_item.save()
    caregiver_bio.save()



#################################################
# Views
##################################################
@login_required
def biospecimen_history(request):
    list_of_historic_caregivers = Caregiver.objects.filter(
        caregiverbiospecimen__status_fk__processed_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__received_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__collected_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__shipped_fk__isnull=False)

    items = CaregiverBiospecimen.objects.filter(caregiver_fk__in=list_of_historic_caregivers)
    return render(request, template_name='biospecimen/biospecimen_history.html', context={'list_of_historic_caregivers':items})

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
def caregiver_biospecimen_item(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    processed_form = ProcessedBiospecimenForm(prefix="processed_form")
    stored_form = StoredBiospecimenForm(prefix="stored_form")
    shipped_form = ShippedBiospecimenForm(prefix="shipped_form")
    received_form = ReceivedBiospecimenForm(prefix="received_form")
    try:
        biospecimen_item =  CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    except:
        raise AssertionError
    return render(request, template_name='biospecimen/caregiver_biospecimen_history.html', context={'biospecimen_item':biospecimen_item,
                                                                                                       'caregiver':caregiver,
                                                                                                       'processed_form':processed_form,
                                                                                                       'stored_form':stored_form,
                                                                                                       'shipped_form':shipped_form,
                                                                                                       'received_form':received_form})

@login_required
def caregiver_biospecimen_initial(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    logging.debug(f"{collection_type} {collection_type in HAIR_SALIVA}")
    if caregiver_bio.status_fk==None and collection_type not in HAIR_SALIVA:
        initial_bio_form = InitialBioForm(prefix="initial_form")
    elif caregiver_bio.status_fk==None and collection_type in HAIR_SALIVA:
        initial_bio_form = InitialBioFormPostNatal(prefix="initial_form")
    else:
        return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    return render(request, template_name='biospecimen/caregiver_biospecimen_initial.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'initial_bio_form':initial_bio_form,
                                                                                                  'collection_type': collection_type.collection_type
                                                                                                    })

@login_required
def caregiver_biospecimen_initial_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    if request.method=="POST" and collection_type not in HAIR_SALIVA:
        form = InitialBioForm(data=request.POST, prefix='initial_form')
        logging.critical(f"{form.is_valid()} {form} {form.errors}")
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
            if collection_type.collection_type in BLOOD_TYPES:
                return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
            else:
                return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    elif request.method=="POST" and collection_type in HAIR_SALIVA:
        form = InitialBioFormPostNatal(data=request.POST, prefix='initial_form')
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
            return redirect("biospecimen:caregiver_biospecimen_entry_hair_urine", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError

    else:
        return redirect("biospecimen:caregiver_biospecimen_initial",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)



@login_required
def caregiver_biospecimen_entry_hair_saliva(request, caregiver_charm_id, caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
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
                                                                                                  'collection_type': collection_type.collection_type,
                                                                                                  'shipped_choice_form': shipped_choice,
                                                                                                  'shipped_wsu_form': shipped_wsu_form,
                                                                                                  'shipped_echo_form':shipped_echo_form,
                                                                                                  'kit_sent_form':kit_sent_form
                                                                                                  })
@login_required()
def caregiver_biospecimen_kit_sent_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
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
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    incentive_form = None
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
        if collection_type.collection_type =='Urine':
            collected_form = CollectedBiospecimenUrineForm(prefix='urine_form')
        elif collection_type in HAIR_SALIVA:
            collected_form = CollectedBiospecimenHairSalivaForm(prefix='hair_saliva_form')
        else:
            collected_form = None
    if collected_item.exists() and caregiver_bio.incentive_fk and not caregiver_bio.incentive_fk.incentive_date:
            incentive_form = IncentiveForm(prefix='incentive_form')
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and caregiver_bio.incentive_fk.incentive_date:
        if collection_type in HAIR_SALIVA and caregiver_bio.incentive_fk.incentive_date:
            shipped_choice = ShippedChoiceEchoForm(prefix='shipped_choice_form')
        else:
            shipped_choice = ShippedChoiceForm(prefix='shipped_choice_form')
    if shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=True):
        logging.debug(f"in shipped to wsu if statement")
        shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
    if shipped_to_echo_item.exists() and shipped_to_echo_item.filter(shipped_date_time__isnull=True):
        logging.debug(f"in shipped to echo if statement")
        shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'collected_form':collected_form,
                                                                                                  'collection_type': collection_type.collection_type,
                                                                                                  'shipped_choice_form': shipped_choice,
                                                                                                  'shipped_wsu_form': shipped_wsu_form,
                                                                                                  'shipped_echo_form':shipped_echo_form,
                                                                                                  'incentive_form': incentive_form
                                                                                                  })

@login_required
def caregiver_biospecimen_entry_blood(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    received_at_wsu_item = ReceivedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    caregiver_bloods = return_caregiver_bloods(caregiver_bio)
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
        logging.debug(blood_dict.get(collection_type.collection_type))
        # disable whatever check box you used to pull the data
        collected_form.fields[str(blood_dict.get(collection_type.collection_type))].initial = True
        collected_form.fields[str(blood_dict.get(collection_type.collection_type))].disabled = True
        # collected_form.fields[str(blood_dict.get(collection_type.collection_type))].widget.attrs['readonly'] = True
    else:
        logging.debug(f"Collected form is none")
        collected_form = None
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and not caregiver_bio.incentive_fk:
        incentive_form = IncentiveForm(prefix='incentive_form')
    elif collected_item.exists() and collected_item.filter(collected_date_time__isnull=False) and caregiver_bio.incentive_fk.incentive_date \
            and not (caregiver_bio.status_fk.shipped_wsu_fk or caregiver_bio.status_fk.shipped_echo_fk):
        logging.critical(f"Made it to shipped choice")
        shipped_choice = ShippedChoiceForm(prefix='shipped_choice_form')
    elif shipped_to_wsu_item.exists() and shipped_to_wsu_item.filter(shipped_date_time__isnull=True):
        logging.critical(f"in shipped to wsu if statement")
        shipped_wsu_form = ShippedtoWSUForm(prefix="shipped_to_wsu_form")
    elif received_at_wsu_item.exists() and received_at_wsu_item.filter(received_date_time__isnull=True):
        received_wsu_form = ReceivedatWSUForm(prefix="received_at_wsu_form")
    elif shipped_to_echo_item.exists() and shipped_to_echo_item.filter(shipped_date_time__isnull=True):
        logging.critical(f"in shipped to echo if statement")
        shipped_echo_form = ShippedtoEchoForm(prefix="shipped_to_echo_form")
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry_blood.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                        'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                        'caregiver_bio': caregiver_bio,
                                                                                                        'collected_form': collected_form,
                                                                                                        'collection_type': collection_type.collection_type,
                                                                                                        'shipped_choice_form': shipped_choice,
                                                                                                        'shipped_wsu_form': shipped_wsu_form,
                                                                                                        'shipped_echo_form': shipped_echo_form,
                                                                                                        'caregiver_bloods': caregiver_bloods,
                                                                                                        'incentive_form':incentive_form,
                                                                                                        'received_wsu_form':received_wsu_form
                                                                                                        })

@login_required
def caregiver_biospecimen_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    logging.debug(f"collection type {collection_type.collection_type} caregiver {caregiver_bio.caregiver_fk.charm_project_identifier}"
                     f"")
    if request.method=="POST":
        if collection_type.collection_type == "Urine":
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
        elif collection_type.collection_type in BLOOD_TYPES:
            logging.debug(f"in the blood if statement")
            form = CollectedBloodForm(data=request.POST,prefix='blood_form')
            logging.debug(f"is form valid {form.is_valid()} \n\nform errors {form.errors} \n\nform {form.data} \n\nrequest.post{request.POST}")
            if form.is_valid():
                #I'm disabling field that references the collection type of the page
                #disabled fields are not passed through the post request, so you have to do it manually :/
                form.cleaned_data[str(blood_dict.get(collection_type.collection_type))] = True
                logging.debug(f"Did form cleaned data update work {form.cleaned_data} ")
                ##if serum is true check that serum exists if exists update if not create and update
                create_or_update_blood_values(true_or_false=form.cleaned_data['serum'],
                                                      collection_type='Serum',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk,
                                                      logged_in_user=request.user)
                create_or_update_blood_values(true_or_false=form.cleaned_data['plasma'],
                                                      collection_type='Plasma',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk,
                                              logged_in_user=request.user)
                create_or_update_blood_values(true_or_false=form.cleaned_data['whole_blood'],
                                                      collection_type='Whole Blood',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk,
                                              logged_in_user=request.user)
                create_or_update_blood_values(true_or_false=form.cleaned_data['buffy_coat'],
                                              collection_type='Buffy Coat',
                                              caregiver_object=caregiver,
                                              trimester_text=caregiver_bio.trimester_fk.trimester,
                                              form_data=form,
                                              caregiver_bio_primary=caregiver_bio_pk,
                                              logged_in_user=request.user)
                create_or_update_blood_values(true_or_false=form.cleaned_data['red_blood_cells'],
                                              collection_type='Red Blood Cells',
                                              caregiver_object=caregiver,
                                              trimester_text=caregiver_bio.trimester_fk.trimester,
                                              form_data=form,
                                              caregiver_bio_primary=caregiver_bio_pk,
                                              logged_in_user=request.user)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
        else:
            raise AssertionError
    else:
        raise AssertionError

def caregiver_biospecimen_incentive_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if request.method=="POST":
        if collection_type in HAIR_SALIVA or collection_type.collection_type=='Urine':
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
        elif collection_type.collection_type in BLOOD_TYPES:
            form = IncentiveForm(data=request.POST, prefix='incentive_form')
            if form.is_valid():
                caregiver_bloods = return_caregiver_bloods(caregiver_bio)
                for item in caregiver_bloods:
                    logging.critical(f"Blood item is {item}")
                    create_or_update_incentive(item.pk, form)
            return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                                caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError

@login_required
def caregiver_shipped_choice_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
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
                logging.critical(f'Shipped to wsu saved')
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'E':
                shipped_to_echo = ShippedECHO.objects.create()
                status.shipped_echo_fk = shipped_to_echo
                status.save()
                logging.critical(f'Shipped to echo saved')
            caregiver_bio.save()
            if collection_type.collection_type in BLOOD_TYPES:
                return redirect("biospecimen:caregiver_biospecimen_entry_blood",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
            else:
                return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

@login_required
def caregiver_biospecimen_shipped_wsu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In wsu post")
    if request.method == "POST":
        if collection_type.collection_type in BLOOD_TYPES:
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
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In received wsu post")
    if request.method == "POST":
        if collection_type.collection_type in BLOOD_TYPES:
            caregiver_bloods = return_caregiver_bloods(caregiver_bio)
            logging.critical(f"care giver bloods {caregiver_bloods}")
            for item in caregiver_bloods:
                logging.critical(f"updating recieved wsu {item.pk}")
                update_received_wsu(caregiver_bio_pk=item.pk, data=request.POST, user_logged_in=request.user)
        return redirect("biospecimen:caregiver_biospecimen_entry_blood", caregiver_charm_id=caregiver_charm_id,
                            caregiver_bio_pk=caregiver_bio_pk)

@login_required
def caregiver_biospecimen_shipped_echo_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_echo_fk = ShippedECHO.objects.get(status=status)
    logging.debug(f"In echo post")
    if request.method == "POST":
        if collection_type.collection_type in BLOOD_TYPES:
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
                logging.debug(f"shipped echo saved")
            return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                                    caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError