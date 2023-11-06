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
    caregivers = Caregiver.objects.filter().prefetch_related("caregivername_set__name_fk__caregivername_set")
    caregivers
    return render(request=request,template_name='reports/caregiver_report.html',context={'caregivers':caregivers})