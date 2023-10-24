import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType,Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Trimester,Project
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import random

logging.basicConfig(level=logging.CRITICAL)

def child_biospecimen_page_initial(request,child_charm_id,child_bio_pk):
    child_bio = ChildBiospecimen.objects.get(pk=child_bio_pk)
    return render(request,template_name='biospecimen/child_biospecimen_initial.html',context={'child_bio':child_bio,
                                                                                              'child_charm_id':child_charm_id,
                                                                                              'child_bio_pk':child_bio_pk})