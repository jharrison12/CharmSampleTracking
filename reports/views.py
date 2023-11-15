import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from dataview.models import Caregiver,CaregiverName,Name,CaregiverAddress
from biospecimen.models import CaregiverBiospecimen
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
def caregiver_report(request):
    caregivers = CaregiverName.objects.filter(status='C').select_related("caregiver_fk")
    caregivers.prefetch_related(Prefetch('caregiveraddress',queryset=CaregiverAddress.objects.filter(status='C')))
    caregivers.prefetch_related('caregiver_fk__caregiveraddress_set__address_fk')
    return render(request=request,template_name='reports/caregiver_report.html',context={'caregivers':caregivers})

@login_required
def biospecimen_report(request):
    caregiver_biospecimens = CaregiverBiospecimen.objects.all().prefetch_related('caregiver_fk')
    return render(request=request,template_name='reports/biospecimen_report.html',context={'caregiver_biospecimens':caregiver_biospecimens,
                                                                                           'caregiver_biospecimen_list':MOTHER_BIOS})