import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from biospecimen.models import CaregiverBiospecimen,Caregiver,Component
from django.db.models import Prefetch
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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
def no_specimen_report_pdf(request):
    caregivers = Caregiver.objects.filter(caregiverbiospecimen__status_fk__isnull=True).exclude(caregiverbiospecimen__status_fk__isnull=False)
    caregivers_distinct = caregivers.values('charm_project_identifier').distinct()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100,100, caregivers)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")




@login_required
def biospecimen_report_urine(request):
    collected_urine = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    shipped_to_wsu_urine = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    received_at_wsu_urine = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='U')
    shipped_to_echo_urine = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='U')
    return render(request=request,template_name='reports/biospecimen_report_urine.html',context={'collected_urine':collected_urine,
                                                                                               'shipped_to_wsu_urine':shipped_to_wsu_urine,
                                                                                               'received_at_wsu_urine':received_at_wsu_urine,
                                                                                               'shipped_to_echo_urine':shipped_to_echo_urine})
@login_required
def collected_report_urine(request):
    collected_urine = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    return render(request=request,template_name='reports/collected_report_urine.html',context={'collected_urine':collected_urine})

@login_required
def shipped_to_wsu_report_urine(request):
    shipped_to_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='U')
    logging.critical(f'collected biospecimen objects {shipped_to_wsu_biospecimen}')
    return render(request=request,template_name='reports/shipped_to_wsu_report_urine.html',context={'shipped_to_wsu_biospecimen':shipped_to_wsu_biospecimen})

@login_required
def received_at_wsu_report_urine(request):
    received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='U')
    logging.critical(f'collected biospecimen objects {received_at_wsu_biospecimen}')
    return render(request=request,template_name='reports/received_at_wsu_report_urine.html',context={'received_at_wsu_biospecimen':received_at_wsu_biospecimen})

@login_required
def shipped_to_echo_report_urine(request):
    shipped_to_echo_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='U')
    logging.critical(f'collected biospecimen objects {shipped_to_echo_biospecimen}')
    return render(request=request,template_name='reports/shipped_to_echo_report_urine.html',context={'shipped_to_echo_biospecimen':shipped_to_echo_biospecimen})


@login_required
def collected_report_blood(request):
    collected_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__collected_fk__isnull=False,status_fk__shipped_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
    components = Component.objects.prefetch_related('caregiver_biospecimen_fk').all()
    collected_biospecimen.prefetch_related('status_fk__collected_fk__component_set').all().order_by('component__component_type')
    return render(request=request,template_name='reports/collected_report_blood.html',context={'collected_biospecimen':collected_biospecimen})

@login_required
def shipped_to_wsu_report_blood(request):
    shipped_to_wsu_biospecimen_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_wsu_fk__isnull=False,status_fk__received_wsu_fk__isnull=True).filter(collection_fk__collection_type='B')
    shipped_to_wsu_biospecimen_blood.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
        'component__component_type')
    return render(request=request, template_name='reports/shipped_to_wsu_report_blood.html',context={'shipped_to_wsu_biospecimen_blood': shipped_to_wsu_biospecimen_blood})

@login_required
def received_at_wsu_report_blood(request):
    received_at_wsu_biospecimen = CaregiverBiospecimen.objects.filter(status_fk__received_wsu_fk__isnull=False,status_fk__shipped_echo_fk__isnull=True).filter(collection_fk__collection_type='B')
    received_at_wsu_biospecimen.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
        'component__component_type')
    logging.critical(f'collected biospecimen objects {received_at_wsu_biospecimen}')
    return render(request=request, template_name='reports/received_at_wsu_report_blood.html',
                  context={'received_at_wsu_biospecimen': received_at_wsu_biospecimen})

def shipped_to_echo_report_blood(request):
    shipped_to_echo_report_blood = CaregiverBiospecimen.objects.filter(status_fk__shipped_echo_fk__isnull=False).filter(collection_fk__collection_type='B')
    shipped_to_echo_report_blood.prefetch_related('status_fk__shipped_wsu_fk__component_set').all().order_by(
        'component__component_type')
    logging.critical(f'collected biospecimen objects {shipped_to_echo_report_blood}')
    return render(request=request, template_name='reports/shipped_to_echo_report_blood.html',
                  context={'shipped_to_echo_report_blood': shipped_to_echo_report_blood})