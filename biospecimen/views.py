import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType,Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Trimester,Project
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm
from django.shortcuts import render,get_object_or_404,redirect
import random

logging.basicConfig(level=logging.CRITICAL)

blood_dict = {'Whole Blood':'whole_blood',
              'Serum':'serum',
              'Plasma':'plasma',
              'Red Blood Cells':'red_blood_cells',
              'Buffy Coat':'buffy_coat'}


def check_for_object_or_return_none(object_name,filter,parameter):
    try:
        return object_name.objects.get(filter=parameter)
    except object_name.DoesNotExist:
        return None

def create_or_update_blood_values(true_or_false,collection_type,caregiver_object,trimester_text,
                                  caregiver_bio_primary,form_data,project='ECHO2',collection_number_object=None):
    if true_or_false:
        trimester = Trimester.objects.get(trimester=trimester_text)
        caregiver_biospecimen = CaregiverBiospecimen.objects.get(pk=caregiver_bio_primary)
        project_object = Project.objects.get(project_name=project)
        collection_object = Collection.objects.get(collection_type_fk__collection_type=collection_type,collection_number_fk__collection_number=collection_number_object)
        logging.debug(f"in the create or update function")
        try:
            biospecimen_object = CaregiverBiospecimen.objects.get(caregiver_fk=caregiver_object,
                                             collection_fk=collection_object,
                                             trimester_fk=trimester,
                                             project_fk__project_name=project)

            biospecimen_object.status_fk.collected_fk.collected_date_time = form_data.cleaned_data['collected_date_time']
            biospecimen_object.status_fk.collected_fk.stored_date_time = form_data.cleaned_data['stored_date_time']
            biospecimen_object.status_fk.collected_fk.processed_date_time = form_data.cleaned_data['processed_date_time']
            biospecimen_object.status_fk.collected_fk.number_of_tubes = form_data.cleaned_data['number_of_tubes']
            biospecimen_object.status_fk.collected_fk.save()
            biospecimen_object.status_fk.save()
            biospecimen_object.save()
            logging.debug(f"Biospecimen object updated")
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
            new_collected.save()
            new_status.save()
            new_biospecimen.status_fk = new_status
            new_biospecimen.save()
            logging.debug(f"Everything created and saved")
    else:
        pass

def biospecimen_history(request):
    list_of_historic_caregivers = Caregiver.objects.filter(
        caregiverbiospecimen__status_fk__processed_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__received_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__collected_fk__isnull=False).filter(
        caregiverbiospecimen__status_fk__shipped_fk__isnull=False)

    items = CaregiverBiospecimen.objects.filter(caregiver_fk__in=list_of_historic_caregivers)
    return render(request,template_name='biospecimen/biospecimen_history.html',context={'list_of_historic_caregivers':items})

def biospecimen_entry(request):
    list_of_echo_2_bio = CaregiverBiospecimen.objects.filter(project_fk__project_name='ECHO2')
    return render(request,template_name='biospecimen/biospecimen_entry.html',context={'list_of_biospecimens':list_of_echo_2_bio})

def caregiver_biospecimen(request,caregiver_charm_id):
    #TODO: Fix this so you're iterating over one queryset and not 15
    caregiver = get_object_or_404(Caregiver,charm_project_identifier=caregiver_charm_id)
    caregiver_collection_query = CaregiverBiospecimen.objects.values('collection_fk__collection_type_fk__collection_type')
    caregiver_collections = list(set(val for dic in caregiver_collection_query for val in dic.values()))
    caregiver_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request, template_name='biospecimen/caregiver_biospecimen.html', context={'caregiver':caregiver,
                                                                                            'caregiver_collections':caregiver_collections,
                                                                                            'caregiver_biospecimens':caregiver_biospecimens})

def child_biospecimen_page(request,child_charm_id):
    child = get_object_or_404(Child,charm_project_identifier=child_charm_id)
    child_collection_query = ChildBiospecimen.objects.values('collection_fk__collection_type_fk__collection_type')
    child_collections = list(set(val for dic in child_collection_query for val in dic.values()))
    child_biospecimens = ChildBiospecimen.objects.filter(child_fk__charm_project_identifier=child_charm_id)
    return render(request, template_name='biospecimen/child_biospecimen.html', context={'child':child,
                                                                                   'child_collections':child_collections,
                                                                                   'child_biospecimens':child_biospecimens})

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

def caregiver_biospecimen_initial(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    logging.debug(f"{caregiver_bio.status_fk}")
    if caregiver_bio.status_fk==None:
        initial_bio_form = InitialBioForm(prefix="initial_form")
    else:
        return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    return render(request, template_name='biospecimen/caregiver_biospecimen_initial.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'initial_bio_form':initial_bio_form,
                                                                                                  'collection_type': collection_type.collection_type
                                                                                                  })

def caregiver_biospecimen_initial_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.filter(pk=caregiver_bio_pk).first()
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if request.method=="POST":
        form = InitialBioForm(data=request.POST, prefix='initial_form')
        if form.is_valid():
            new_status = Status()
            caregiver_bio.status_fk = new_status
            new_status.save()
            caregiver_bio.save()
            if form.cleaned_data['collected_not_collected']=='C':
                new_collected = Collected.objects.create()
                new_status.collected_fk = new_collected
            elif form.cleaned_data['collected_not_collected']=='N':
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected']=='X':
                new_no_consent = NoConsent.objects.create()
                new_status.no_consent_fk = new_no_consent
            new_status.save()
            caregiver_bio.save()
        else:
            raise AssertionError
        return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        return redirect("biospecimen:caregiver_biospecimen_initial",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)

def caregiver_biospecimen_entry(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    collected_item = Collected.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_wsu_item = ShippedWSU.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    shipped_to_echo_item = ShippedECHO.objects.filter(status__caregiverbiospecimen=caregiver_bio)
    collected_form = None
    shipped_choice = None
    shipped_wsu_form = None
    shipped_echo_form = None
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=True):
        if collection_type.collection_type =='Urine':
            collected_form = CollectedBiospecimenUrineForm(prefix='urine_form')
        elif collection_type.collection_type in ('Whole Blood','Serum','Plasma', 'Buffy Coat','Red Blood Cells'):

            collected_form = CollectedBloodForm(prefix='blood_form')
            logging.critical(blood_dict.get(collection_type.collection_type))
            #disable whatever check box you used to pull the data
            collected_form.fields[str(blood_dict.get(collection_type.collection_type))].initial = True
            collected_form.fields[str(blood_dict.get(collection_type.collection_type))].disabled = True

        else:
            collected_form = None
    if collected_item.exists() and collected_item.filter(collected_date_time__isnull=False):
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
                                                                                                  'shipped_echo_form':shipped_echo_form
                                                                                                  })

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
                collected_urine.stored_date_time = form.cleaned_data['stored_date_time']
                collected_urine.number_of_tubes = form.cleaned_data['number_of_tubes']
                collected_urine.save()
                caregiver_bio.save()
        if collection_type.collection_type in ('Whole Blood','Serum','Plasma', 'Buffy Coat','Red Blood Count'):
            logging.debug(f"in the blood if statement")
            form = CollectedBloodForm(data=request.POST,prefix='blood_form')
            logging.debug(f"is form valid {form.is_valid()} form errors {form.errors} form {form.data} request.post{request.POST}")
            if form.is_valid():
                ##if serum is true check that serum exists if exists update if not create and update
                create_or_update_blood_values(true_or_false=form.cleaned_data['serum'],
                                                      collection_type='Serum',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk)
                create_or_update_blood_values(true_or_false=form.cleaned_data['plasma'],
                                                      collection_type='Plasma',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk)
                create_or_update_blood_values(true_or_false=form.cleaned_data['whole_blood'],
                                                      collection_type='Whole Blood',
                                                      caregiver_object=caregiver,
                                                      trimester_text=caregiver_bio.trimester_fk.trimester,
                                                      form_data=form,
                                                      caregiver_bio_primary=caregiver_bio_pk)
                create_or_update_blood_values(true_or_false=form.cleaned_data['buffy_coat'],
                                              collection_type='Buffy Coat',
                                              caregiver_object=caregiver,
                                              trimester_text=caregiver_bio.trimester_fk.trimester,
                                              form_data=form,
                                              caregiver_bio_primary=caregiver_bio_pk)
                create_or_update_blood_values(true_or_false=form.cleaned_data['red_blood_cells'],
                                              collection_type='Red Blood Cells',
                                              caregiver_object=caregiver,
                                              trimester_text=caregiver_bio.trimester_fk.trimester,
                                              form_data=form,
                                              caregiver_bio_primary=caregiver_bio_pk)

        return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

def caregiver_shipped_choice_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    if request.method=="POST":
        logging.debug(f"post is {request.POST}")
        form = ShippedChoiceForm(data=request.POST, prefix='shipped_choice_form')
        logging.debug(f"is shipped form valid{form.is_valid()}  {form.errors} {form}")
        if form.is_valid():
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'W':
                shipped_to_wsu = ShippedWSU.objects.create()
                status.shipped_wsu_fk = shipped_to_wsu
                status.save()
                logging.debug(f'Shipped to wsu saved')
            if form.cleaned_data['shipped_to_wsu_or_echo'] == 'E':
                shipped_to_echo = ShippedECHO.objects.create()
                status.shipped_echo_fk = shipped_to_echo
                status.save()
                logging.debug(f'Shipped to echo saved')
        caregiver_bio.save()
        return redirect("biospecimen:caregiver_biospecimen_entry",caregiver_charm_id=caregiver_charm_id,caregiver_bio_pk=caregiver_bio_pk)
    else:
        raise AssertionError

def caregiver_biospecimen_shipped_wsu_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_wsu_fk = ShippedWSU.objects.get(status=status)
    logging.debug(f"In wsu post")
    if request.method == "POST":
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
        return redirect("biospecimen:caregiver_biospecimen_entry", caregiver_charm_id=caregiver_charm_id,
                        caregiver_bio_pk=caregiver_bio_pk)

    else:
        raise AssertionError

def caregiver_biospecimen_shipped_echo_post(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    status = Status.objects.get(caregiverbiospecimen=caregiver_bio)
    shipped_echo_fk = ShippedECHO.objects.get(status=status)
    logging.debug(f"In echo post")
    if request.method == "POST":
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