from django.shortcuts import render,get_object_or_404
from dataview.models import Caregiver,Name,CaregiverName,\
    Address,Email,CaregiverEmail,Phone,CaregiverPhone,SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Survey,Project,CaregiverSurvey,Incentive,IncentiveType


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
    caregiver_email_primary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='PR').first()
    caregiver_email_secondary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='SD').first()
    caregiver_phone_primary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='PR').first()
    caregiver_phone_secondary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='SD').first()
    caregiver_social_media = SocialMedia.objects.filter(caregiversocialmedia__caregiver_fk__charm_project_identifier=caregiver_charm_id)

    return render(request=request,template_name='dataview/caregiver_info.html',context={'caregiver':caregiver,
                                                                                        'caregiver_name':caregiver_name,
                                                                                        'caregiver_address':caregiver_address,
                                                                                        'caregiver_email_primary':caregiver_email_primary,
                                                                                        'caregiver_email_secondary':caregiver_email_secondary,
                                                                                        'caregiver_phone_primary':caregiver_phone_primary,
                                                                                        'caregiver_phone_secondary': caregiver_phone_secondary,
                                                                                        'caregiver_social_media': caregiver_social_media})

def caregiver_contact(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    ##TODO is there a better way of filtering?
    contact_a_name = Name.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='PR').first()
    contact_a_phone = Phone.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='PR').first()
    contact_a_address = Address.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='PR').first()
    contact_a_email = Email.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='PR').first()
    contact_b_name = Name.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='SD').first()
    contact_b_phone = Phone.objects.filter(
        caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id) \
        .filter(caregiverpersonalcontact__caregiver_contact_type='SD').first()
    contact_b_address = Address.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='SD').first()
    contact_b_email = Email.objects.filter(caregiverpersonalcontact__caregiver_fk__charm_project_identifier=caregiver_charm_id)\
        .filter(caregiverpersonalcontact__caregiver_contact_type='SD').first()
    return render(request=request,template_name='dataview/caregiver_contact.html',context={'caregiver':caregiver,
                                                                                           'contact_a_name':contact_a_name,
                                                                                           'contact_a_phone':contact_a_phone,
                                                                                           'contact_a_address':contact_a_address,
                                                                                           'contact_a_email':contact_a_email,
                                                                                           'contact_b_name':contact_b_name,
                                                                                           'contact_b_phone':contact_b_phone,
                                                                                           'contact_b_address':contact_b_address,
                                                                                           'contact_b_email':contact_b_email})

def caregiver_survey(request,caregiver_charm_id):
    caregiver_surveys = CaregiverSurvey.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request,template_name='dataview/caregiver_survey.html',context={'caregiver_surveys':caregiver_surveys})