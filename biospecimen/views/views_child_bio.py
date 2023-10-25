import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType,Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Trimester,Project,\
    KitSent
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,InitialBioFormChild,KitSentForm
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import random


logging.basicConfig(level=logging.CRITICAL)

@login_required
def child_biospecimen_page_initial(request,child_charm_id,child_bio_pk):
    child_bio = ChildBiospecimen.objects.get(pk=child_bio_pk)
    initial_bio_form = None
    kit_sent_form = None
    logging.critical(f"request.post {request.POST}")
    if request.method=="POST" and 'initial_bio_form_button' in request.POST:
        form = InitialBioFormChild(data=request.POST, prefix='initial_bio_form')
        if form.is_valid():
            new_status = Status()
            child_bio.status_fk = new_status
            new_status.save()
            child_bio.save()
            if form.cleaned_data['collected_not_collected_kit_sent']=='N':
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected_kit_sent']=='X':
                new_no_consent = NoConsent.objects.create()
                new_status.no_consent_fk = new_no_consent
            if form.cleaned_data['collected_not_collected_kit_sent']=='K':
                kit_sent = KitSent.objects.create()
                new_status.kit_sent_fk = kit_sent
            new_status.save()
            child_bio.save()
            return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                            child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'kit_sent_form_button' in request.POST:
        form = KitSentForm(data=request.POST, prefix="kit_sent_form")
        logging.critical(f"Is kit sent form valid {form.is_valid()}")
        if form.is_valid():
            child_bio.status_fk.kit_sent_fk.kit_sent_date = form.cleaned_data['kit_sent_date']
            child_bio.status_fk.kit_sent_fk.save()
            child_bio.status_fk.save()
            child_bio.save()
            return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    else:
        if child_bio.status_fk==None:
            initial_bio_form = InitialBioFormChild(prefix="initial_bio_form")
        elif child_bio.status_fk and child_bio.status_fk.kit_sent_fk and not child_bio.status_fk.kit_sent_fk.kit_sent_date:
            kit_sent_form = KitSentForm(prefix="kit_sent_form")
    return render(request,template_name='biospecimen/child_biospecimen_initial.html',context={'child_bio':child_bio,
                                                                                              'child_charm_id':child_charm_id,
                                                                                              'child_bio_pk':child_bio_pk,
                                                                                              'initial_bio_form':initial_bio_form,
                                                                                              'kit_sent_form':kit_sent_form})