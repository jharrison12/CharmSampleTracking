from django.shortcuts import render,get_object_or_404
from dataview.models import Caregiver,Name,CaregiverName,\
    Address,Email,CaregiverEmail,Phone,CaregiverPhone,SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Survey,Project,CaregiverSurvey,Incentive,IncentiveType,CaregiverBiospecimen


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
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_biospecimens = CaregiverBiospecimen.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    biospecimen_serum_one = caregiver_biospecimens.filter(collection_fk__collection_type='Serum').filter(collection_fk__collection_number=1).first()
    biospecimen_serum_two = caregiver_biospecimens.filter(collection_fk__collection_type='Serum').filter(collection_fk__collection_number=2).first()
    biospecimen_plasma_one = caregiver_biospecimens.filter(collection_fk__collection_type='Plasma').filter(collection_fk__collection_number=1).first()
    biospecimen_plasma_two = caregiver_biospecimens.filter(collection_fk__collection_type='Plasma').filter(collection_fk__collection_number=2).first()
    biospecimen_bloodspots_one = caregiver_biospecimens.filter(collection_fk__collection_type='Bloodspots').filter(collection_fk__collection_number=1).first()
    biospecimen_bloodspots_two = caregiver_biospecimens.filter(collection_fk__collection_type='Bloodspots').filter(collection_fk__collection_number=2).first()
    biospecimen_whole_blood_one = caregiver_biospecimens.filter(collection_fk__collection_type='Whole Blood').filter(collection_fk__collection_number=1).first()
    biospecimen_whole_blood_two = caregiver_biospecimens.filter(collection_fk__collection_type='Whole Blood').filter(collection_fk__collection_number=2).first()
    biospecimen_buffy_coat_one = caregiver_biospecimens.filter(collection_fk__collection_type='Buffy Coat').filter(collection_fk__collection_number=1).first()
    biospecimen_buffy_coat_two = caregiver_biospecimens.filter(collection_fk__collection_type='Buffy Coat').filter(collection_fk__collection_number=2).first()
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    return render(request,template_name='dataview/caregiver_biospecimen.html',context={'biospecimens': caregiver_biospecimens,
                                                                                       'biospecimen_serum_one': biospecimen_serum_one,
                                                                                       'biospecimen_serum_two':biospecimen_serum_two,
                                                                                       'biospecimen_plasma_one': biospecimen_plasma_one,
                                                                                       'biospecimen_plasma_two':biospecimen_plasma_two,
                                                                                       'biospecimen_bloodspots_one':biospecimen_bloodspots_one,
                                                                                       'biospecimen_bloodspots_two':biospecimen_bloodspots_two,
                                                                                       'biospecimen_whole_blood_one': biospecimen_whole_blood_one,
                                                                                       'biospecimen_whole_blood_two': biospecimen_whole_blood_two,
                                                                                       'biospecimen_buffy_coat_one': biospecimen_buffy_coat_one,
                                                                                       'biospecimen_buffy_coat_two':biospecimen_buffy_coat_two,
                                                                                       'caregiver':caregiver,
                                                                                       'caregiver_name': caregiver_name})