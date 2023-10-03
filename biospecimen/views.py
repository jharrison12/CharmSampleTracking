import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm
from django.shortcuts import render,get_object_or_404,redirect
import random

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
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

def caregiver_biospecimen_item(request,caregiver_charm_id,biospecimen,collection_num):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    processed_form = ProcessedBiospecimenForm(prefix="processed_form")
    stored_form = StoredBiospecimenForm(prefix="stored_form")
    shipped_form = ShippedBiospecimenForm(prefix="shipped_form")
    received_form = ReceivedBiospecimenForm(prefix="received_form")
    collection_number = CollectionNumber.objects.get(collection_number=collection_num)
    collection_type = CollectionType.objects.get(collection_type=biospecimen.capitalize())
    logging.debug(f"biospecimen capitalize {biospecimen.capitalize()}")
    biospecimen = get_object_or_404(Collection,collection_type_fk=collection_type,
                                    collection_number_fk=collection_number)
    logging.debug(f'bio is {biospecimen}')
    try:
        biospecimen_item = CaregiverBiospecimen.objects.get(caregiver_fk__charm_project_identifier=caregiver_charm_id,
                                                       collection_fk=biospecimen)
    except:
        new_status = Status.objects.create()
        biospecimen_item = CaregiverBiospecimen.objects.create(caregiver_fk=caregiver,
                                                               status_fk=new_status,
                                                               collection_fk=biospecimen,
                                                               #TODO fix this
                                                               biospecimen_id=random.randint(1000, 9999),
                                                               )


    return render(request, template_name='biospecimen/caregiver_biospecimen_history.html', context={'biospecimen_item':biospecimen_item,
                                                                                                       'caregiver':caregiver,
                                                                                                       'processed_form':processed_form,
                                                                                                       'stored_form':stored_form,
                                                                                                       'shipped_form':shipped_form,
                                                                                                       'received_form':received_form})


def caregiver_biospecimen_entry(request,caregiver_charm_id,caregiver_bio_pk):
    caregiver_bio = CaregiverBiospecimen.objects.get(pk=caregiver_bio_pk)
    collection_type = CollectionType.objects.get(collection__caregiverbiospecimen=caregiver_bio)
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if collection_type.collection_type =='Urine':
        collected_form = CollectedBiospecimenUrineForm()
    else:
        collected_form = None
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'charm_project_identifier':caregiver_charm_id,
                                                                                                  'caregiver_bio_pk':caregiver_bio_pk,
                                                                                                  'caregiver_bio': caregiver_bio,
                                                                                                  'collected_form':collected_form
                                                                                                  })

