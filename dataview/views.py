import logging

from django.shortcuts import render,get_object_or_404,redirect
from dataview.models import Caregiver,Name,CaregiverName,\
    Address,Email,CaregiverEmail,Phone,CaregiverPhone,SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Survey,Project,CaregiverSurvey,Incentive,IncentiveType,CaregiverBiospecimen
from dataview.forms import CaregiverBiospecimenForm,IncentiveForm

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def home_page(request):
    return render(request=request,template_name='dataview/home.html')

def caregiver(request):
    caregivers = Caregiver.objects.all()
    return render(request=request, template_name='dataview/caregiver.html', context={'mother_or_caregiver':caregivers})

def caregiver_info(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    caregiver_address = Address.objects.filter(caregiveraddress__caregiver_fk__charm_project_identifier=caregiver_charm_id).first()
    caregiver_email_primary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='PR').first()
    caregiver_email_secondary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='SD').first()
    caregiver_phone_primary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='PR').first()
    caregiver_phone_secondary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='SD').first()
    #caregiver_social_media = SocialMedia.objects.filter(caregiversocialmedia__caregiver_fk__charm_project_identifier=caregiver_charm_id)
    caregiver_social_media = CaregiverSocialMedia.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    contact_a = CaregiverPersonalContact.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiver_contact_type='PR').first()
    contact_b = CaregiverPersonalContact.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiver_contact_type='SD').first()

    return render(request=request,template_name='dataview/caregiver_info.html',context={'caregiver':caregiver,
                                                                                        'caregiver_name':caregiver_name,
                                                                                        'caregiver_address':caregiver_address,
                                                                                        'caregiver_email_primary':caregiver_email_primary,
                                                                                        'caregiver_email_secondary':caregiver_email_secondary,
                                                                                        'caregiver_phone_primary':caregiver_phone_primary,
                                                                                        'caregiver_phone_secondary': caregiver_phone_secondary,
                                                                                        'caregiver_social_media': caregiver_social_media,
                                                                                        'contact_a': contact_a,
                                                                                        'contact_b': contact_b
                                                                                        })

def caregiver_survey(request,caregiver_charm_id):
    caregiver_surveys = CaregiverSurvey.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request,template_name='dataview/caregiver_survey.html',context={'caregiver_surveys':caregiver_surveys,
                                                                                  'charm_id':caregiver_charm_id})
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
    return render(request,template_name='dataview/caregiver_biospecimen.html',context={'biospecimens': caregiver_biospecimens,
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
        logging.critical(f" post is {request.POST}")
        bio_form = CaregiverBiospecimenForm(data=request.POST,prefix='bio_form')
        incentive_form = IncentiveForm(data=request.POST, prefix='incentive_form')
        logging.critical(f" form is {bio_form.data}")
        logging.critical(f"form is valid {bio_form.is_valid()}\n")
        logging.critical(f"form errors {bio_form.errors}\n\n")
        #form.full_clean()
        if bio_form.is_valid() and incentive_form.is_valid():
            incentive = incentive_form.save()
            bio_form_final = bio_form.save(commit=False)
            bio_form_final.incentive_fk = incentive
            #logging.critical(f"bio form incentive {bio_form.incentive_fk}\n")
            logging.critical(f" post form is {bio_form.data}\n")
            logging.critical(f"form is valid {bio_form.is_valid()}\n")
            bio_form_final.save()
            return redirect('dataview:caregiver_biospecimen',caregiver_charm_id=caregiver_charm_id)
    else:
        incentive_form = IncentiveForm(prefix='incentive_form')
        bio_form = CaregiverBiospecimenForm(initial={"caregiver_fk":caregiver},prefix='bio_form')
    return render(request,template_name='dataview/caregiver_biospecimen_entry.html', context={'bio_form':bio_form,
                                                                                              'incentive_form':incentive_form,
                                                                                              'charm_project_identifier':caregiver_charm_id})