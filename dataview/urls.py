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
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/biospecimen/$", dataviews.caregiver_biospecimen,name='caregiver_biospecimen'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/biospecimen/entry/$", dataviews.caregiver_biospecimen_entry,name='caregiver_biospecimen_entry')
]
