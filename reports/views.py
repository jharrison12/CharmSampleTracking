import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from dataview.models import Caregiver,CaregiverName,Name
from biospecimen.models import CaregiverBiospecimen

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
@login_required
def home_page(request):
    return render(request=request,template_name='reports/home.html')

@login_required
def caregiver_report(request):
    caregivers = CaregiverName.objects.filter(status='C').prefetch_related("caregiver_fk").prefetch_related("caregiver_fk__caregiveraddress_set").filter(status='C')
    return render(request=request,template_name='reports/caregiver_report.html',context={'caregivers':caregivers})

@login_required
def biospecimen_report(request):
    caregiver_biospecimens = CaregiverBiospecimen.objects.all().prefetch_related('caregiver_fk')
    return render(request=request,template_name='reports/biospecimen_report.html',context={'caregiver_biospecimens':caregiver_biospecimens})