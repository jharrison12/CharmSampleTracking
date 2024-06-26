import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from biospecimen.models import CaregiverBiospecimen,Caregiver,Component,BloodSpotCard
from django.db.models import Prefetch
import io
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required

logging.basicConfig(level=logging.CRITICAL)

MOTHER_BIOS = [
    {'collection_type':'Saliva','age_category':'ZF'},
    {'collection_type':'Hair','age_category':'ZF'}
]

# Create your views here.
@login_required
def home_page(request):
    return render(request=request,template_name='reports/home.html')

@login_required
def biospecimen_report(request):
    caregiver_biospecimens = CaregiverBiospecimen.objects.all().prefetch_related('caregiver_fk')
    return render(request=request,template_name='reports/biospecimen_report.html',context={'caregiver_biospecimens':caregiver_biospecimens,
                                                                                           'caregiver_biospecimen_list':MOTHER_BIOS})

@login_required
@staff_member_required
def no_specimen_report(request):
    caregivers = Caregiver.objects.filter(caregiverbiospecimen__status_fk__isnull=True).exclude(caregiverbiospecimen__status_fk__isnull=False)
    caregivers_distinct = caregivers.values('charm_project_identifier').distinct()
    return render(request=request,template_name='reports/no_specimen_report.html',context={'caregivers':caregivers_distinct,
                                                                                           'caregiver_biospecimen_list':MOTHER_BIOS})

@login_required
@staff_member_required
def biospecimen_report_urine(request):
    collected_urine = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__collected_fk__collected_date_time__isnull=False,status_fk__processed_fk__isnull=True).filter(collection_fk__collection_type='U')
    processed_urine = CaregiverBiospecimen.objects.filter(status_fk__processed_fk__isnull=False,status_fk__processed_fk__processed_aliquoted_date_time__isnull=False).filter(collection_fk__collection_type='U')
    frozen_urine = CaregiverBiospecimen.objects.filter(status_fk__frozen_fk__isnull=False,status_fk__frozen_fk__freezer_placed_date_time__isnull=False).filter(collection_fk__collection_type='U')
    shipped_to_wsu_urine = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    received_at_wsu_urine = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='U')
    shipped_to_echo_urine = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='U')
    return render(request=request,template_name='reports/biospecimen_report_urine.html',context={'collected_urine':collected_urine,
                                                                                               'processed_urine':processed_urine,
                                                                                               'frozen_urine':frozen_urine,
                                                                                               'shipped_to_wsu_urine':shipped_to_wsu_urine,
                                                                                               'received_at_wsu_urine':received_at_wsu_urine,
                                                                                               'shipped_to_echo_urine':shipped_to_echo_urine
                                                                                                 })

@login_required
@staff_member_required
def biospecimen_report_blood(request):
    collected_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__collected_fk__collected_date_time__isnull=False, status_fk__frozen_fk__isnull=True).filter(collection_fk__collection_type='B')
    collected_blood.prefetch_related('bloodtube_set').all()
    processed_biospecimen_blood = CaregiverBiospecimen.objects.filter(status_fk__frozen_fk__isnull=True,status_fk__processed_blood_fk__isnull=False).filter(collection_fk__collection_type='B')
    processed_biospecimen_blood.prefetch_related('bloodtube_set').all()
    shipped_to_wsu_biospecimen_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
    shipped_to_wsu_biospecimen_blood.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
        'component__component_type')
    received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='B')
    received_at_wsu_biospecimen.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
        'component__component_type')
    shipped_to_echo_report_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='B')
    shipped_to_echo_report_blood.prefetch_related('status_fk__shipped_echo_fk__component_set').all().order_by(
        'component__component_type')
    return render(request=request,template_name='reports/biospecimen_report_blood.html',context={'collected_blood':collected_blood,
                                                                                                 'processed_biospecimen_blood':processed_biospecimen_blood,
                                                                                               'shipped_to_wsu_biospecimen_blood':shipped_to_wsu_biospecimen_blood,
                                                                                               'received_at_wsu_biospecimen':received_at_wsu_biospecimen,
                                                                                               'shipped_to_echo_report_blood':shipped_to_echo_report_blood})

@login_required
def collected_report_urine(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        collected_urine = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    else:
        collected_urine = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='U').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    return render(request=request,template_name='reports/collected_report_urine.html',context={'collected_urine':collected_urine})

@login_required
def shipped_to_wsu_report_urine(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        shipped_to_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    else:
        shipped_to_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True)\
            .filter(collection_fk__collection_type='U').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    return render(request=request,template_name='reports/shipped_to_wsu_report_urine.html',context={'shipped_to_wsu_biospecimen':shipped_to_wsu_biospecimen})

@login_required
def received_at_wsu_report_urine(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='U')
    else:
        received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True)\
            .filter(collection_fk__collection_type='U').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    logging.debug(f'collected biospecimen objects {received_at_wsu_biospecimen}')
    return render(request=request,template_name='reports/received_at_wsu_report_urine.html',context={'received_at_wsu_biospecimen':received_at_wsu_biospecimen})

@login_required
def shipped_to_echo_report_urine(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        shipped_to_echo_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False)\
            .filter(collection_fk__collection_type='U')
    else:
        shipped_to_echo_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False) \
            .filter(collection_fk__collection_type='U').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    logging.debug(f'collected biospecimen objects {shipped_to_echo_biospecimen}')
    return render(request=request,template_name='reports/shipped_to_echo_report_urine.html',context={'shipped_to_echo_biospecimen':shipped_to_echo_biospecimen})

@login_required
def collected_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        collected_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
        collected_blood.prefetch_related('status_fk__collected_fk__component_set').all().order_by('component__component_type')
    else:
        collected_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True)\
            .filter(collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
        collected_blood.prefetch_related('status_fk__collected_fk__component_set').all().order_by(
            'component__component_type')
    return render(request=request,template_name='reports/collected_report_blood.html',context={'collected_blood':collected_blood})

@login_required
def processed_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        processed_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__processed_blood_fk__isnull=False,status_fk__frozen_fk__isnull=True).filter(collection_fk__collection_type='B')
    else:
        processed_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__processed_blood_fk__isnull=False,status_fk__frozen_fk__isnull=True)\
            .filter(collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    return render(request=request,template_name='reports/processed_report_blood.html',context={'processed_blood':processed_blood})

@login_required
def frozen_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        frozen_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__processed_blood_fk__isnull=False,status_fk__frozen_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
        # blood_card_frozen = BloodSpotCard.objects.get(caregiver_bio_fk=)
    else:
        frozen_blood = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__processed_blood_fk__isnull=False,status_fk__frozen_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True)\
            .filter(collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
    return render(request=request,template_name='reports/frozen_report_blood.html',context={'frozen_blood':frozen_blood})

@login_required
def shipped_to_wsu_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        shipped_to_wsu_biospecimen_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
        shipped_to_wsu_biospecimen_blood.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
            'component__component_type')
    else:
        shipped_to_wsu_biospecimen_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True)\
            .filter(collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
        shipped_to_wsu_biospecimen_blood.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
            'component__component_type')
    return render(request=request, template_name='reports/shipped_to_wsu_report_blood.html',context={'shipped_to_wsu_biospecimen_blood': shipped_to_wsu_biospecimen_blood})

@login_required
def received_at_wsu_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='B')
        received_at_wsu_biospecimen.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
            'component__component_type')
    else:
        received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,
                                                                          status_fk__shipped_echo_fk__isnull=True).filter(
            collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
        received_at_wsu_biospecimen.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
            'component__component_type')
    return render(request=request, template_name='reports/received_at_wsu_report_blood.html',
                  context={'received_at_wsu_biospecimen': received_at_wsu_biospecimen})

@login_required
def shipped_to_echo_report_blood(request):
    if request.user.is_staff or request.user.recruitment_location=='A':
        shipped_to_echo_report_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='B')
        shipped_to_echo_report_blood.prefetch_related('status_fk__shipped_echo_fk__component_set').all().order_by(
            'component__component_type')
    else:
        shipped_to_echo_report_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False)\
            .filter(collection_fk__collection_type='B').filter(caregiver_fk__recruitment_location=request.user.recruitment_location)
        shipped_to_echo_report_blood.prefetch_related('status_fk__shipped_echo_fk__component_set').all().order_by(
            'component__component_type')

    return render(request=request, template_name='reports/shipped_to_echo_report_blood.html',
                  context={'shipped_to_echo_report_blood': shipped_to_echo_report_blood})