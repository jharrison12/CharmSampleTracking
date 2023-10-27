import logging

from dataview.models import Caregiver,Name, Child
from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status, Processed, Outcome, Collection, Stored, \
    Shipped, Received,CollectionNumber,CollectionType,Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Trimester,Project,\
    KitSent
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ProcessedBiospecimenForm,StoredBiospecimenForm,\
ShippedBiospecimenForm, ReceivedBiospecimenForm,CollectedBiospecimenUrineForm,InitialBioForm,ShippedChoiceForm,ShippedtoWSUForm,\
    ShippedtoEchoForm,CollectedBloodForm,InitialBioFormChild,KitSentForm,CollectedChildUrineForm
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
    collected_child_urine_form = None
    shipped_choice_form = None
    shipped_to_echo_form = None
    shipped_to_wsu_form = None
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

    elif request.method=="POST" and 'collected_form_button' in request.POST:
        form = CollectedChildUrineForm(data=request.POST,prefix='collected_child_urine_form')
        logging.critical(f"Is collected urine form valid {form.is_valid()}")
        if form.is_valid():
            collected = Collected()
            child_bio.status_fk.collected_fk = collected
            collected.received_date = form.cleaned_data['date_received']
            collected.number_of_tubes = form.cleaned_data['number_of_tubes']
            ##todo this will need to be the incentive model!!!
            collected.incentive_date = form.cleaned_data['number_of_tubes']
            collected.in_person_remote = form.cleaned_data['in_person_remote']
            collected.logged_by = request.user
            collected.save()
            child_bio.status_fk.save()
            child_bio.save()
        else:
            raise form.errors
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'shipped_choice_form_button' in request.POST:
        form = ShippedChoiceForm(data=request.POST, prefix='child_shipped_choice_form')
        logging.critical(f"is shipped choice valid {form.is_valid()} {form.errors}")
        if form.is_valid():
            if form.cleaned_data['shipped_to_wsu_or_echo']=='W':
                shipped_to_wsu = ShippedWSU.objects.create(shipped_by=request.user)
                child_bio.status_fk.shipped_wsu_fk = shipped_to_wsu
                child_bio.status_fk.shipped_wsu_fk.save()
                child_bio.status_fk.save()
                child_bio.save()
                logging.critical(f'Shipped to wsu saved')
            elif form.cleaned_data['shipped_to_wsu_or_echo']=='E':
                shipped_to_echo = ShippedECHO.objects.create()
                child_bio.status_fk.shipped_echo_fk = shipped_to_echo
                child_bio.status_fk.shipped_echo_fk.save()
                child_bio.status_fk.save()
                child_bio.save()
                logging.critical(f'Shipped to echo saved')
            else:
                raise AssertionError
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'shipped_to_echo_form_button' in request.POST:
        form = ShippedtoEchoForm(data=request.POST, prefix='child_shipped_to_echo_form')
        if form.is_valid():
            child_bio.status_fk.shipped_echo_fk.shipped_date_time = form.cleaned_data['shipped_date_and_time']
            child_bio.status_fk.shipped_echo_fk.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'shipped_to_wsu_form_button' in request.POST:
        form = ShippedtoWSUForm(data=request.POST, prefix='child_shipped_to_wsu_form')
        logging.critical(f"is shipped choice valid {form.is_valid()} {form.errors}")
        if form.is_valid():
            child_bio.status_fk.shipped_wsu_fk.shipped_date_time = form.cleaned_data['shipped_date_and_time']
            child_bio.status_fk.shipped_wsu_fk.number_of_tubes= form.cleaned_data['number_of_tubes']
            child_bio.status_fk.shipped_wsu_fk.courier = form.cleaned_data['courier']
            child_bio.status_fk.shipped_wsu_fk.tracking_number = form.cleaned_data['tracking_number']
            child_bio.status_fk.shipped_wsu_fk.shipped_by = request.user
            child_bio.status_fk.shipped_wsu_fk.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    else:
        if child_bio.status_fk==None:
            initial_bio_form = InitialBioFormChild(prefix="initial_bio_form")
        elif child_bio.status_fk and child_bio.status_fk.kit_sent_fk and not child_bio.status_fk.kit_sent_fk.kit_sent_date:
            kit_sent_form = KitSentForm(prefix="kit_sent_form")
        elif child_bio.status_fk and child_bio.status_fk.kit_sent_fk and child_bio.status_fk.kit_sent_fk.kit_sent_date and not child_bio.status_fk.collected_fk:
            collected_child_urine_form = CollectedChildUrineForm(prefix="collected_child_urine_form")
        elif child_bio.status_fk and child_bio.status_fk.collected_fk and child_bio.status_fk.collected_fk.received_date and not (child_bio.status_fk.shipped_echo_fk or child_bio.status_fk.shipped_wsu_fk):
            shipped_choice_form = ShippedChoiceForm(prefix="child_shipped_choice_form")
        elif child_bio.status_fk.shipped_echo_fk and not child_bio.status_fk.shipped_echo_fk.shipped_date_time:
            shipped_to_echo_form = ShippedtoEchoForm(prefix="child_shipped_to_echo_form")
        elif child_bio.status_fk.shipped_wsu_fk and not child_bio.status_fk.shipped_wsu_fk.shipped_date_time:
            shipped_to_wsu_form = ShippedtoWSUForm(prefix="child_shipped_to_wsu_form")
        else:
            pass
    return render(request,template_name='biospecimen/child_biospecimen_initial.html',context={'child_bio':child_bio,
                                                                                              'child_charm_id':child_charm_id,
                                                                                              'child_bio_pk':child_bio_pk,
                                                                                              'initial_bio_form':initial_bio_form,
                                                                                              'kit_sent_form':kit_sent_form,
                                                                                              'collected_child_urine_form':collected_child_urine_form,
                                                                                              'shipped_choice_form':shipped_choice_form,
                                                                                              'shipped_to_echo_form': shipped_to_echo_form,
                                                                                              'shipped_to_wsu_form':shipped_to_wsu_form})