import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from dataview.models import Caregiver,CaregiverName,Name,CaregiverAddress
from biospecimen.models import CaregiverBiospecimen
from django.db.models import Prefetch
from django.shortcuts import render
logging.basicConfig(level=logging.CRITICAL)

@login_required
def home_page(request):
    return render(request=request,template_name='lists/home.html')

@login_required
def incentive_list(request):
    return render(request=request, template_name='lists/incentive_list.html')

@login_required
def incentive_list_caregiver_biospecimen(request):
    return render(request=request,template_name='lists/incentive_list_caregiver_biospecimen.html')

@login_required
def incentive_list_caregiver_charm_id(request):
    return render(request=request,template_name='lists/incentive_list_caregiver_charm_id.html')

# Create your views here.
