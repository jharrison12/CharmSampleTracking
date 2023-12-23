import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from biospecimen.models import CaregiverBiospecimen,Collection,Caregiver
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
    list_of_ids = Caregiver.objects.filter(caregiverbiospecimen__incentive_fk__isnull=False).values_list("charm_project_identifier",flat=True).distinct()
    caregivers = Caregiver.objects.filter(caregiverbiospecimen__incentive_fk__isnull=False)
    list_of_biospecimens =  [c[0] for c in Collection.CollectionType.choices]
    return render(request=request,template_name='lists/incentive_list_caregiver_charm_id.html',context={'list_of_ids':list_of_ids,
                                                                                                        'list_of_biospecimens':list_of_biospecimens})

# Create your views here.
