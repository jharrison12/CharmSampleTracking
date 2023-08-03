from django.shortcuts import render,get_object_or_404
from dataview.models import Caregiver,Name,CaregiverName,Address,Email,CaregiverEmail

# Create your views here.
def home_page(request):
    return render(request=request,template_name='dataview/home.html')

def caregiver(request):
    caregivers = Caregiver.objects.all()
    return render(request=request, template_name='dataview/caregiver.html', context={'mother_or_caregiver':caregivers})

def caregiver_info(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    caregiver_address = get_object_or_404(Address, caregiveraddress__caregiver_fk__charm_project_identifier=caregiver_charm_id)
    caregiver_email = get_object_or_404(Email,caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request=request,template_name='dataview/caregiver_info.html',context={'caregiver':caregiver,
                                                                                        'caregiver_name':caregiver_name,
                                                                                        'caregiver_address':caregiver_address,
                                                                                        'caregiver_email':caregiver_email})