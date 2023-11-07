import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from dataview.models import Caregiver,CaregiverName,Name

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
@login_required
def home_page(request):
    return render(request=request,template_name='reports/home.html')

@login_required
def caregiver_report(request):
    caregivers = Caregiver.objects.filter()
    caregivers = CaregiverName.objects.filter(status='C').prefetch_related("caregiver_fk").prefetch_related("caregiver_fk__caregiveraddresshistory_set__caregiver_address_fk")
    return render(request=request,template_name='reports/caregiver_report.html',context={'caregivers':caregivers})