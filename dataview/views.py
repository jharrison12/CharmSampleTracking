from django.shortcuts import render
from dataview.models import Caregiver,Name,CaregiverName

# Create your views here.
def home_page(request):
    return render(request=request,template_name='dataview/home.html')

def caregiver(request):
    caregivers = Caregiver.objects.all()
    return render(request=request, template_name='dataview/caregiver.html', context={'mother_or_caregiver':caregivers})

def caregiver_info(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.get(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request=request,template_name='dataview/caregiver_info.html',context={'caregiver':caregiver,'caregiver_name':caregiver_name})