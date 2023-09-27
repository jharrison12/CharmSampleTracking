import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen,ChildBiospecimen,Status,Processed,Outcome,Collection,Stored,Shipped
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm
from django.shortcuts import render,get_object_or_404,redirect

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def caregiver_biospecimen(request,caregiver_charm_id):
    #TODO: Fix this so you're iterating over one queryset and not 15
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    caregiver_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    biospecimen_serum = caregiver_biospecimens.filter(collection_fk__collection_type='Serum')
    biospecimen_plasma = caregiver_biospecimens.filter(collection_fk__collection_type='Plasma')
    biospecimen_bloodspots = caregiver_biospecimens.filter(collection_fk__collection_type='Bloodspots')
    biospecimen_whole_blood = caregiver_biospecimens.filter(collection_fk__collection_type='Whole Blood')
    biospecimen_buffy_coat = caregiver_biospecimens.filter(collection_fk__collection_type='Buffy Coat')
    biospecimen_red_blood_cells = caregiver_biospecimens.filter(collection_fk__collection_type='Red Blood Cells')
    biospecimen_urines = caregiver_biospecimens.filter(collection_fk__collection_type='Urine')
    biospecimen_hair = caregiver_biospecimens.filter(collection_fk__collection_type='Hair')
    biospecimen_toenail = caregiver_biospecimens.filter(collection_fk__collection_type='Toenail')
    biospecimen_saliva = caregiver_biospecimens.filter(collection_fk__collection_type='Saliva')
    biospecimen_placenta = caregiver_biospecimens.filter(collection_fk__collection_type='Placenta')
    return render(request, template_name='biospecimen/caregiver_biospecimen.html', context={'biospecimens': caregiver_biospecimens,
                                                                                       'biospecimen_serum': biospecimen_serum,
                                                                                       'biospecimen_plasma': biospecimen_plasma,
                                                                                       'biospecimen_bloodspots':biospecimen_bloodspots,
                                                                                       'biospecimen_whole_blood': biospecimen_whole_blood,
                                                                                       'biospecimen_buffy_coat': biospecimen_buffy_coat,
                                                                                       'biospecimen_red_blood_cells': biospecimen_red_blood_cells,
                                                                                       'biospecimen_urines':biospecimen_urines,
                                                                                       'biospecimen_hair':biospecimen_hair,
                                                                                       'biospecimen_toenail':biospecimen_toenail,
                                                                                       'biospecimen_saliva':biospecimen_saliva,
                                                                                                               'biospecimen_placenta':biospecimen_placenta,
                                                                                                               'caregiver':caregiver,
                                                                                                               'caregiver_name': caregiver_name})

def caregiver_biospecimen_blood_spots(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    processed_form = ProcessedBiospecimenForm(prefix="processed_form")
    stored_form = StoredBiospecimenForm(prefix="stored_form")
    shipped_form = ShippedBiospecimenForm(prefix="shipped_form")
    try:
        blood_spots = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier=caregiver_charm_id,
                                                       collection_fk__collection_type='Bloodspots')
    except:
        blood_spots = None


    return render(request, template_name='biospecimen/caregiver_biospecimen_blood_spots.html',context={'blood_spots':blood_spots,
                                                                                                       'caregiver':caregiver,
                                                                                                       'processed_form':processed_form,
                                                                                                       'stored_form':stored_form,
                                                                                                       'shipped_form':shipped_form})

def caregiver_biospecimen_processed_post(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    collection_type = Collection.objects.get(collection_type='Bloodspots')
    if request.method == "POST":
        processed_form = ProcessedBiospecimenForm(data=request.POST, prefix="processed_form")
        if processed_form.is_valid():
            logging.critical(f"is valid {processed_form.is_valid()}")
            ##TODO add function to receive biospecimen id
            blood_spots, created = CaregiverBiospecimen.objects.get_or_create(caregiver_fk=caregiver,
                                                                              collection_fk=collection_type,
                                                                              biospecimen_id='TEST')
            processed_item = Processed.objects.create()
            status_item = Status.objects.create(processed_fk=processed_item,stored_fk=None)
            logging.critical(f'status item {status_item}')
            blood_spots.status_fk = status_item
            processed_item.collected_date_time = processed_form.cleaned_data['collected_date_time']
            processed_item.outcome_fk = Outcome.objects.get(outcome__iexact=processed_form.cleaned_data['outcome_fk'])
            processed_item.quantity = processed_form.cleaned_data['quantity']
            processed_item.logged_date_time = processed_form.cleaned_data['logged_date_time']
            processed_item.save()
            blood_spots.save()
            status_item.save()
            logging.critical("everything saved")
        return redirect('biospecimen:caregiver_biospecimen_blood_spots', caregiver.charm_project_identifier)
    else:
        raise AssertionError


def caregiver_biospecimen_stored_post(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    collection_type = Collection.objects.get(collection_type='Bloodspots')
    processed_item = Processed.objects.get(status__caregiverbiospecimen__collection_fk_id=collection_type,status__caregiverbiospecimen__caregiver_fk_id=caregiver)
    if request.method == "POST":
        stored_form = StoredBiospecimenForm(data=request.POST, prefix="stored_form")
        if stored_form.is_valid():
            logging.critical(f"is valid {stored_form.is_valid()}")
            ##TODO add function to receive biospecimen id
            blood_spots = CaregiverBiospecimen.objects.get(caregiver_fk=caregiver,
                                                                              collection_fk=collection_type,
                                                                              )
            stored_item = Stored.objects.create()
            status_item = Status.objects.get(processed_fk=processed_item,caregiverbiospecimen__caregiver_fk=caregiver)
            status_item.stored_fk = stored_item
            logging.critical(f'status item {status_item}')
            blood_spots.status_fk = status_item
            stored_item.stored_date_time = stored_form.cleaned_data['stored_date_time']
            stored_item.outcome_fk = Outcome.objects.get(outcome__iexact=stored_form.cleaned_data['outcome_fk'])
            stored_item.quantity = stored_form.cleaned_data['quantity']
            stored_item.logged_date_time = stored_form.cleaned_data['logged_date_time']
            stored_item.save()
            blood_spots.save()
            status_item.save()
            logging.critical("everything saved")
        return redirect('biospecimen:caregiver_biospecimen_blood_spots', caregiver.charm_project_identifier)
    else:
        raise AssertionError

def caregiver_biospecimen_shipped_post(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    collection_type = Collection.objects.get(collection_type='Bloodspots')
    processed_item = Processed.objects.get(status__caregiverbiospecimen__collection_fk_id=collection_type,
                                           status__caregiverbiospecimen__caregiver_fk_id=caregiver)
    stored_item = Stored.objects.get(status__caregiverbiospecimen__collection_fk_id=collection_type,
                                           status__caregiverbiospecimen__caregiver_fk_id=caregiver)
    if request.method == "POST":
        shipped_form = ShippedBiospecimenForm(data=request.POST, prefix="shipped_form")
        if shipped_form.is_valid():
            logging.critical(f"is valid {shipped_form.is_valid()}")
            ##TODO add function to receive biospecimen id
            blood_spots = CaregiverBiospecimen.objects.get(caregiver_fk=caregiver,
                                                           collection_fk=collection_type,
                                                           )
            shipped = Shipped.objects.create()
            status_item = Status.objects.get(processed_fk=processed_item, caregiverbiospecimen__caregiver_fk=caregiver,stored_fk=stored_item)
            status_item.shipped_fk = shipped
            logging.critical(f'status item {status_item}')
            blood_spots.status_fk = status_item
            shipped.shipped_date_time = shipped_form.cleaned_data['shipped_date_time']
            shipped.outcome_fk = Outcome.objects.get(outcome__iexact=shipped_form.cleaned_data['outcome_fk'])
            shipped.quantity = shipped_form.cleaned_data['quantity']
            shipped.logged_date_time = shipped_form.cleaned_data['logged_date_time']
            shipped.courier = shipped_form.cleaned_data['courier']
            shipped.shipping_number = shipped_form.cleaned_data['shipping_number']
            stored_item.save()
            blood_spots.save()
            status_item.save()
            shipped.save()
            logging.critical("everything saved")
        return redirect('biospecimen:caregiver_biospecimen_blood_spots', caregiver.charm_project_identifier)
    else:
        raise AssertionError

def caregiver_biospecimen_entry(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if request.method=="POST":
        bio_form = CaregiverBiospecimenForm(data=request.POST,prefix='bio_form')
        incentive_form = IncentiveForm(data=request.POST, prefix='incentive_form')
        if bio_form.is_valid() and incentive_form.is_valid():
            incentive = incentive_form.save()
            bio_form_final = bio_form.save(commit=False)
            bio_form_final.incentive_fk = incentive
            bio_form_final.save()
            return redirect('biospecimen:caregiver_biospecimen',caregiver_charm_id=caregiver_charm_id)
    else:
        incentive_form = IncentiveForm(prefix='incentive_form')
        bio_form = CaregiverBiospecimenForm(initial={"caregiver_fk":caregiver},prefix='bio_form')
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'bio_form':bio_form,
                                                                                              'incentive_form':incentive_form,
                                                                                              'charm_project_identifier':caregiver_charm_id})


def child_biospecimen_page(request,child_charm_id):
    child = get_object_or_404(Child,charm_project_identifier=child_charm_id)
    child_collection_query = ChildBiospecimen.objects.values('collection_fk__collection_type')
    child_collections = list(set(val for dic in child_collection_query for val in dic.values()))
    child_biospecimens = ChildBiospecimen.objects.filter(child_fk__charm_project_identifier=child_charm_id)
    return render(request, template_name='biospecimen/child_biospecimen.html', context={'child':child,
                                                                                   'child_collections':child_collections,
                                                                                   'child_biospecimens':child_biospecimens})