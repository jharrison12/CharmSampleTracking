import logging


from biospecimen.models import CaregiverBiospecimen, ChildBiospecimen, Status,\
    Collected,NotCollected,NoConsent,ShippedWSU,ShippedECHO,Project,\
    KitSent,Declined,Incentive,AgeCategory,Collection
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm,ShippedtoEchoForm,InitialBioFormPostNatal,KitSentForm,CollectedChildUrineStoolForm,CollectedChildBloodSpotForm,\
CollectedChildBloodSpotHairFormOneYear,ShippedtoWSUFormChild,InitialBioFormChildTooth,CollectedChildToothForm,\
    ShippedChoiceEchoForm,DeclinedForm,ReceivedatWSUForm
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random


logging.basicConfig(level=logging.debug)

NOT_COLLECTED = 'N'
DECLINED = 'X'
KIT_SENT = 'K'
URINE_AND_STOOL = ['U','O']
BLOODSPOT = 'S'
BLOODSPOT_AND_HAIR = ['S','H']
TOOTH = Collection.CollectionType.TOOTH

ZERO_TO_FIVE = 'ZF'
TWELVE_TO_THIRTEEN_MONTHS = 'TT'
SIX_TO_TEN_YEARS = AgeCategory.AgeCategoryChoice.SIX_TO_TEN_YEARS

@login_required
def child_biospecimen_page_initial(request,child_charm_id,child_bio_pk):
    child_bio = ChildBiospecimen.objects.get(pk=child_bio_pk)
    collection_type = child_bio.collection_fk.collection_type
    collection_type_display = child_bio.collection_fk.get_collection_type_display()
    initial_bio_form = None
    kit_sent_form = None
    collected_child_form = None
    shipped_choice_form = None
    shipped_to_echo_form = None
    shipped_to_wsu_form = None
    declined_form = None
    incentive_form = None
    received_at_wsu_form = None
    logging.debug(f"request.post {request.POST}")
    if request.method=="POST" and 'initial_bio_form_button' in request.POST:
        form = InitialBioFormPostNatal(data=request.POST, prefix='initial_bio_form')
        if form.is_valid():
            new_status = Status()
            child_bio.status_fk = new_status
            new_status.save()
            child_bio.save()
            if form.cleaned_data['collected_not_collected_kit_sent']==NOT_COLLECTED:
                new_not_collected = NotCollected.objects.create()
                new_status.not_collected_fk = new_not_collected
            elif form.cleaned_data['collected_not_collected_kit_sent']==DECLINED:
                new_declined = Declined.objects.create()
                new_status.declined_fk = new_declined
            if form.cleaned_data['collected_not_collected_kit_sent']==KIT_SENT:
                kit_sent = KitSent.objects.create()
                new_status.kit_sent_fk = kit_sent
            new_status.save()
            child_bio.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                            child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'kit_sent_form_button' in request.POST:
        form = KitSentForm(data=request.POST, prefix="kit_sent_form")
        logging.debug(f"Is kit sent form valid {form.is_valid()}")
        if form.is_valid():
            child_bio.status_fk.kit_sent_fk.kit_sent_date = form.cleaned_data['kit_sent_date']
            child_bio.biospecimen_id = form.cleaned_data['echo_biospecimen_id']
            child_bio.status_fk.kit_sent_fk.save()
            child_bio.status_fk.save()
            child_bio.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'collected_form_button' in request.POST:
        if collection_type in URINE_AND_STOOL and child_bio.age_category_fk.age_category==ZERO_TO_FIVE:
            form = CollectedChildUrineStoolForm(data=request.POST,prefix='collected_child_form')
            logging.debug(f"Is  form valid {form.is_valid()} form errors {form.errors}")
            if form.is_valid():
                collected = Collected()
                child_bio.status_fk.collected_fk = collected
                collected.received_date = form.cleaned_data['date_received']
                collected.number_of_tubes = form.cleaned_data['number_of_tubes']
                collected.in_person_remote = form.cleaned_data['in_person_remote']
                collected.logged_by = request.user
                collected.save()
                child_bio.status_fk.save()
                child_bio.save()
        elif collection_type==BLOODSPOT and child_bio.age_category_fk.age_category==ZERO_TO_FIVE:
            form = CollectedChildBloodSpotForm(data=request.POST, prefix='collected_child_form')
            logging.debug(f"Is  form valid {form.is_valid()} form errors {form.errors}")
            if form.is_valid():
                collected = Collected()
                child_bio.status_fk.collected_fk = collected
                collected.received_date = form.cleaned_data['date_received']
                collected.number_of_cards = form.cleaned_data['number_of_cards']
                ##todo this will need to be the incentive model!!!
                collected.in_person_remote = form.cleaned_data['in_person_remote']
                collected.logged_by = request.user
                collected.save()
                child_bio.status_fk.save()
                child_bio.save()
        elif collection_type in BLOODSPOT_AND_HAIR and child_bio.age_category_fk.age_category==TWELVE_TO_THIRTEEN_MONTHS:
            form = CollectedChildBloodSpotHairFormOneYear(data=request.POST, prefix='collected_child_form')
            logging.debug(f"Is  form valid {form.is_valid()} form errors {form.errors}")
            if form.is_valid():
                collected = Collected()
                child_bio.status_fk.collected_fk = collected
                collected.received_date = form.cleaned_data['date_received']
                ##todo this will need to be the incentive model!!!
                collected.in_person_remote = form.cleaned_data['in_person_remote']
                collected.logged_by = request.user
                collected.save()
                child_bio.status_fk.save()
                child_bio.save()
        elif collection_type==TOOTH and child_bio.age_category_fk.age_category==SIX_TO_TEN_YEARS:
            form = CollectedChildToothForm(data=request.POST, prefix='collected_child_form')
            logging.debug(f"Is  form valid {form.is_valid()} form errors {form.errors}")
            if form.is_valid():
                collected = Collected()
                child_bio.status_fk.collected_fk = collected
                collected.collected_date_time = form.cleaned_data['date_collected']
                ##todo this will need to be the incentive model!!!
                collected.logged_by = request.user
                collected.save()
                child_bio.status_fk.save()
                child_bio.save()
        else:
            AssertionError
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'incentive_form_button' in request.POST:
        form = IncentiveForm(data=request.POST, prefix="child_incentive_form")
        logging.debug(f'incentive form {form} request post is {request.POST}')
        if form.is_valid():
            incentive_one = form.save()
            child_bio.incentive_fk = incentive_one
            child_bio.incentive_fk.save()
            child_bio.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method == "POST" and 'declined_form_button' in request.POST:
            form = DeclinedForm(data=request.POST,prefix='declined_form')
            logging.debug(f"is declined valid {form.is_valid()} {form.errors} {form}")
            if form.is_valid():
                child_bio.status_fk.declined_fk.declined_date = form.cleaned_data['declined_date']
                child_bio.status_fk.declined_fk.save()
                child_bio.status_fk.save()
                child_bio.save()
            return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                                child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'shipped_to_echo_form_button' in request.POST:
        form = ShippedtoEchoForm(data=request.POST, prefix='child_shipped_to_echo_form')
        if form.is_valid():
            shipped_to_echo_item = ShippedECHO()
            shipped_to_echo_item.shipped_date_time = form.cleaned_data['shipped_date_and_time']
            child_bio.status_fk.shipped_echo_fk = shipped_to_echo_item
            child_bio.status_fk.shipped_echo_fk.save()
            child_bio.status_fk.save()
            child_bio.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'shipped_to_wsu_form_button' in request.POST:
        form = ShippedtoWSUFormChild(data=request.POST, prefix='child_shipped_to_wsu_form')
        logging.debug(f"is shipped choice valid {form.is_valid()} {form.errors}")
        if form.is_valid():
            shipped_to_wsu_item = ShippedWSU()
            shipped_to_wsu_item.shipped_date_time = form.cleaned_data['shipped_date_and_time']
            child_bio.status_fk.shipped_wsu_fk = shipped_to_wsu_item
            child_bio.status_fk.shipped_wsu_fk.save()
            child_bio.status_fk.save()
            child_bio.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    elif request.method=="POST" and 'received_at_wsu_form_button' in request.POST:
        form = ReceivedatWSUForm(data=request.POST, prefix='child_received_at_wsu_form')
        logging.debug(f"is received at wsu valid {form.is_valid()} {form.errors} {form}")
        if form.is_valid():
            received_at_wsu = form.save()
            child_bio.status_fk.received_wsu_fk = received_at_wsu
            child_bio.status_fk.received_wsu_fk.save()
            child_bio.status_fk.save()
        return redirect("biospecimen:child_biospecimen_page_initial", child_charm_id=child_charm_id,
                        child_bio_pk=child_bio_pk)
    else:
        if child_bio.status_fk==None:
            if collection_type==TOOTH:
                initial_bio_form = InitialBioFormChildTooth(prefix="initial_bio_form")
            else:
                initial_bio_form = InitialBioFormPostNatal(prefix="initial_bio_form")
        elif child_bio.status_fk and child_bio.status_fk.kit_sent_fk and not child_bio.status_fk.kit_sent_fk.kit_sent_date:
            kit_sent_form = KitSentForm(prefix="kit_sent_form")
        elif child_bio.status_fk and child_bio.status_fk.kit_sent_fk and child_bio.status_fk.kit_sent_fk.kit_sent_date and not child_bio.status_fk.collected_fk:
            if child_bio.age_category_fk.age_category==ZERO_TO_FIVE:
                if collection_type in URINE_AND_STOOL:
                    collected_child_form = CollectedChildUrineStoolForm(prefix="collected_child_form")
                elif collection_type==BLOODSPOT:
                    collected_child_form = CollectedChildBloodSpotForm(prefix="collected_child_form")
            elif child_bio.age_category_fk.age_category==TWELVE_TO_THIRTEEN_MONTHS:
                if collection_type in BLOODSPOT_AND_HAIR:
                    collected_child_form = CollectedChildBloodSpotHairFormOneYear(prefix="collected_child_form")
            elif child_bio.age_category_fk.age_category==SIX_TO_TEN_YEARS:
                #I am keeping this logic in case they want to add more biospecimens
                if collection_type==TOOTH:
                    collected_child_form = CollectedChildToothForm(prefix="collected_child_form")
        elif child_bio.status_fk and child_bio.status_fk.collected_fk and not child_bio.incentive_fk:
            incentive_form = IncentiveForm(prefix="child_incentive_form")
            logging.debug(f"{child_bio.status_fk} {child_bio.status_fk.collected_fk} ")
        elif child_bio.status_fk and child_bio.status_fk.collected_fk\
            and (child_bio.status_fk.collected_fk.received_date or child_bio.status_fk.collected_fk.collected_date_time)\
                and not (child_bio.status_fk.shipped_echo_fk or child_bio.status_fk.shipped_wsu_fk or child_bio.status_fk.shipped_msu_fk):
            if collection_type in URINE_AND_STOOL or (collection_type==BLOODSPOT and child_bio.age_category_fk.age_category==ZERO_TO_FIVE):
                shipped_to_wsu_form = ShippedtoWSUFormChild(prefix="child_shipped_to_wsu_form")
            elif collection_type in BLOODSPOT_AND_HAIR or collection_type==TOOTH:
                shipped_to_echo_form = ShippedtoEchoForm(prefix="child_shipped_to_echo_form")
        elif child_bio.status_fk.shipped_wsu_fk and child_bio.status_fk.shipped_wsu_fk.shipped_date_time and not child_bio.status_fk.received_wsu_fk:
            received_at_wsu_form = ReceivedatWSUForm(prefix="child_received_at_wsu_form")
        elif child_bio.status_fk.received_wsu_fk and child_bio.status_fk.received_wsu_fk.received_date_time:
            logging.debug(f"in shipped to echo if statement")
            shipped_to_echo_form = ShippedtoEchoForm(prefix="child_shipped_to_echo_form")
        elif child_bio.status_fk.declined_fk:
            declined_form = DeclinedForm(prefix="declined_form",initial={'declined_date':timezone.now().date()})
        else:
            pass
    logging.debug(f"RIGHT BEFORE RETURN {shipped_to_echo_form} {child_bio.status_fk }")
    logging.debug(f"Collection type {collection_type}")
    return render(request,template_name='biospecimen/child_biospecimen_initial.html',context={'child_bio':child_bio,
                                                                                              'child_charm_id':child_charm_id,
                                                                                              'child_bio_pk':child_bio_pk,
                                                                                              'initial_bio_form':initial_bio_form,
                                                                                              'kit_sent_form':kit_sent_form,
                                                                                              'collected_child_form':collected_child_form,
                                                                                              'shipped_choice_form':shipped_choice_form,
                                                                                              'shipped_to_echo_form': shipped_to_echo_form,
                                                                                              'shipped_to_wsu_form':shipped_to_wsu_form,
                                                                                              'declined_form':declined_form,
                                                                                              'incentive_form': incentive_form,
                                                                                              'received_at_wsu_form':received_at_wsu_form,
                                                                                              'collection_type_display':collection_type_display,
                                                                                              'urine_stool': ['U','O'],
                                                                                              'TOOTH':'E',
                                                                                              'BLOODSPOT':'S',
                                                                                              'ZERO_TO_FIVE_MONTHS':'ZF'})