"""
URL configuration for CharmSampleTracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path,re_path
from dataview import views as dataviews
import dataview

app_name = "dataview"
urlpatterns = [
    re_path(r"^caregiver/$", dataviews.caregiver, name='caregivers'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/$", dataviews.caregiver_info,name='caregiver_info'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/survey/$", dataviews.caregiver_survey,name='caregiver_survey'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/consentitem/$", dataviews.caregiver_consent_item,name='caregiver_consent_item'),
    re_path(r"^child/$", dataviews.child,name='child'),
    re_path(r"^child/(?P<child_charm_id>\w+)/$", dataviews.child_information_page,name='child_information_page'),
    re_path(r"^child/(?P<child_charm_id>\w+)/survey/$", dataviews.child_survey_page,name='child_survey_page'),
    re_path(r"^child/(?P<child_charm_id>\w+)/assent/$", dataviews.child_assent_page,name='child_assent_page'),
    re_path(r"^child/(?P<child_charm_id>\w+)/biospecimen/$", dataviews.child_biospecimen_page,name='child_biospecimen_page')
]
