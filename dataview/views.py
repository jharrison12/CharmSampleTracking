import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect

from dataview.forms import CaregiverBiospecimenForm,IncentiveForm

logging.basicConfig(level=logging.CRITICAL)

# Create your views here.
@login_required
def home_page(request):
    return render(request=request,template_name='dataview/home.html')

@login_required
def caregiver(request):
    caregivers = Caregiver.objects.all()
    return render(request=request, template_name='dataview/caregiver.html', context={'mother_or_caregiver':caregivers})

@login_required
def caregiver_info(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    caregiver_name = Name.objects.filter(caregivername__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregivername__status='C').first()
    caregiver_address = Address.objects.filter(caregiveraddress__caregiver_fk__charm_project_identifier=caregiver_charm_id).first()
    caregiver_email_primary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='PR').first()
    caregiver_email_secondary = Email.objects.filter(caregiveremail__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiveremail__email_type='SD').first()
    caregiver_phone_primary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='PR').first()
    caregiver_phone_secondary = Phone.objects.filter(caregiverphone__caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiverphone__phone_type='SD').first()
    caregiver_social_media = CaregiverSocialMedia.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    contact_a = CaregiverPersonalContact.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiver_contact_type='PR').first()
    contact_b = CaregiverPersonalContact.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id).filter(caregiver_contact_type='SD').first()
    caregiver_pregnancy_info = Pregnancy.objects.filter(mother_fk__caregiver_fk=caregiver)

    return render(request=request,template_name='dataview/caregiver_info.html',context={'caregiver':caregiver,
                                                                                        'caregiver_name':caregiver_name,
                                                                                        'caregiver_address':caregiver_address,
                                                                                        'caregiver_email_primary':caregiver_email_primary,
                                                                                        'caregiver_email_secondary':caregiver_email_secondary,
                                                                                        'caregiver_phone_primary':caregiver_phone_primary,
                                                                                        'caregiver_phone_secondary': caregiver_phone_secondary,
                                                                                        'caregiver_social_media': caregiver_social_media,
                                                                                        'contact_a': contact_a,
                                                                                        'contact_b': contact_b,
                                                                                        'caregiver_pregnancies': caregiver_pregnancy_info
                                                                                        })
@login_required
def caregiver_survey(request,caregiver_charm_id):
    caregiver_surveys = CaregiverSurvey.objects.filter(caregiver_fk__charm_project_identifier=caregiver_charm_id)
    return render(request,template_name='dataview/caregiver_survey.html',context={'caregiver_surveys':caregiver_surveys,
                                                                                  'charm_id':caregiver_charm_id})
@login_required
def caregiver_consent_item(request,caregiver_charm_id):
    caregiver = Caregiver.objects.get(charm_project_identifier=caregiver_charm_id)
    consent_items = ConsentItem.objects.filter(caregiver_fk=caregiver)
    return render(request,template_name='dataview/caregiver_consent_item.html',context={'consent_items':consent_items,
                                                                                        'caregiver':caregiver})
@login_required
def child(request):
    children = Child.objects.all()
    return render(request,template_name='dataview/child.html', context={'children':children})

@login_required
def child_information_page(request, child_charm_id):
    child = get_object_or_404(Child, charm_project_identifier=child_charm_id)
    child_name = Name.objects.filter(childname__child_fk=child).filter(childname__status='C').first()
    child_address = Address.objects.filter(childaddress__child_fk=child).first()
    caregiver_relation = CaregiverChildRelation.objects.filter(child_fk__charm_project_identifier=child_charm_id).filter(caregiver_fk__primarycaregiver__child=child).first()
    return render(request,template_name='dataview/child_information.html',context={'child':child,
                                                                                   'child_name':child_name,
                                                                                   'child_address':child_address,
                                                                                   'caregiver_relation':caregiver_relation})
@login_required
def child_survey_page(request,child_charm_id):
    child = get_object_or_404(Child, charm_project_identifier=child_charm_id)
    child_survey = ChildSurvey.objects.filter(child_fk__charm_project_identifier=child_charm_id)
    return render(request,template_name='dataview/child_survey.html',context={'child':child,
                                                                              'child_survey':child_survey})
@login_required
def child_assent_page(request,child_charm_id):
    child = get_object_or_404(Child, charm_project_identifier=child_charm_id)
    child_assent = ChildAssent.objects.filter(child_fk__charm_project_identifier=child_charm_id)
    return render(request,template_name='dataview/child_assent.html',context={'child':child,
                                                                              'child_assent':child_assent})

