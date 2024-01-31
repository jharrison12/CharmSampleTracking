import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from biospecimen.models import CaregiverBiospecimen,Caregiver,Component
from django.db.models import Prefetch

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
def no_specimen_report(request):
    caregivers = Caregiver.objects.filter(caregiverbiospecimen__status_fk__isnull=True).exclude(caregiverbiospecimen__status_fk__isnull=False)
    caregivers_distinct = caregivers.values('charm_project_identifier').distinct()
    return render(request=request,template_name='reports/no_specimen_report.html',context={'caregivers':caregivers_distinct,
                                                                                           'caregiver_biospecimen_list':MOTHER_BIOS})

@login_required
def collected_report_urine(request):
    collected_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    logging.critical(f'collected biospecimen objects {collected_biospecimen}')
    return render(request=request,template_name='reports/collected_report_urine.html',context={'collected_biospecimen':collected_biospecimen})

@login_required
def collected_report_blood(request):
    collected_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
    components = Component.objects.prefetch_related('caregiver_biospecimen_fk').all()
    collected_biospecimen.prefetch_related('status_fk__collected_fk__component_set').all().order_by('component__component_type')
    logging.critical(f'prefetch related {components.values}')
    # logging.critical(f'prefetch related using collected bio {components2}')
    # logging.critical(f'collected biospecimen objects {collected_biospecimen.component_set}')
    return render(request=request,template_name='reports/collected_report_blood.html',context={'collected_biospecimen':collected_biospecimen})