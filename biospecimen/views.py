from dataview.models import Caregiver,Name,CaregiverBiospecimen
from biospecimen.forms import CaregiverBiospecimenForm,IncentiveForm
from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
def caregiver_biospecimen(request,caregiver_charm_id):
    #TODO: Fix this so you're iterating over one queryset and not 15
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    caregiver_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    biospecimen_serum = caregiver_biospecimens.filter(collection_fk__collection_type='Serum')
    biospecimen_plasma = caregiver_biospecimens.filter(collection_fk__collection_type='Plasma')
    biospecimen_bloodspots = caregiver_biospecimens.filter(collection_fk__collection_type='Bloodspots')
    biospecimen_whole_blood = caregiver_biospecimens.filter(collection_fk__collection_type='Whole Blood')
    biospecimen_buffy_coat = caregiver_biospecimens.filter(collection_fk__collection_type='Buffy Coat')
    biospecimen_red_blood_cells = caregiver_biospecimens.filter(collection_fk__collection_type='Red Blood Cells')
    biospecimen_urines = caregiver_biospecimens.filter(collection_fk__collection_type='Urine')
    biospecimen_hair = caregiver_biospecimens.filter(collection_fk__collection_type='Hair')
    biospecimen_toenail = caregiver_biospecimens.filter(collection_fk__collection_type='Toenail')
    biospecimen_saliva = caregiver_biospecimens.filter(collection_fk__collection_type='Saliva')
    biospecimen_placenta = caregiver_biospecimens.filter(collection_fk__collection_type='Placenta')
    return render(request, template_name='biospecimen/caregiver_biospecimen.html', context={'biospecimens': caregiver_biospecimens,
                                                                                       'biospecimen_serum': biospecimen_serum,
                                                                                       'biospecimen_plasma': biospecimen_plasma,
                                                                                       'biospecimen_bloodspots':biospecimen_bloodspots,
                                                                                       'biospecimen_whole_blood': biospecimen_whole_blood,
                                                                                       'biospecimen_buffy_coat': biospecimen_buffy_coat,
                                                                                       'biospecimen_red_blood_cells': biospecimen_red_blood_cells,
                                                                                       'biospecimen_urines':biospecimen_urines,
                                                                                       'biospecimen_hair':biospecimen_hair,
                                                                                       'biospecimen_toenail':biospecimen_toenail,
                                                                                       'biospecimen_saliva':biospecimen_saliva,
                                                                                                               'biospecimen_placenta':biospecimen_placenta,
                                                                                                               'caregiver':caregiver,
                                                                                                               'caregiver_name': caregiver_name})

def caregiver_biospecimen_entry(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    if request.method=="POST":
        bio_form = CaregiverBiospecimenForm(data=request.POST,prefix='bio_form')
        incentive_form = IncentiveForm(data=request.POST, prefix='incentive_form')
        if bio_form.is_valid() and incentive_form.is_valid():
            incentive = incentive_form.save()
            bio_form_final = bio_form.save(commit=False)
            bio_form_final.incentive_fk = incentive
            bio_form_final.save()
            return redirect('biospecimen:caregiver_biospecimen',caregiver_charm_id=caregiver_charm_id)
    else:
        incentive_form = IncentiveForm(prefix='incentive_form')
        bio_form = CaregiverBiospecimenForm(initial={"caregiver_fk":caregiver},prefix='bio_form')
    return render(request, template_name='biospecimen/caregiver_biospecimen_entry.html', context={'bio_form':bio_form,
                                                                                              'incentive_form':incentive_form,
                                                                                              'charm_project_identifier':caregiver_charm_id})