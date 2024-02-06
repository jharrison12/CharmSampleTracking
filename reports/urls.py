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
from reports import views as reports


app_name = "reports"
urlpatterns = [
    re_path(r"^$", reports.home_page, name='reports_home'),
    re_path(r"^biospecimen_report/$", reports.biospecimen_report, name='biospecimen_report'),
    re_path(r"^no_specimen_report/$", reports.no_specimen_report, name='no_specimen_report'),
    re_path(r"^collected_report/urine/$", reports.collected_report_urine, name='collected_report_urine'),
    re_path(r"^collected_report/blood/$", reports.collected_report_blood, name='collected_report_blood'),
    re_path(r"^shipped_to_wsu_report/urine/$", reports.shipped_to_wsu_report_urine, name='shipped_to_wsu_report_urine'),
    re_path(r"^shipped_to_wsu_report/blood/$", reports.shipped_to_wsu_report_blood, name='shipped_to_wsu_report_blood'),
    re_path(r"^received_at_wsu_report/urine/$", reports.received_at_wsu_report_urine, name='received_at_wsu_report_urine'),
    re_path(r"^received_at_wsu_report/blood/$", reports.received_at_wsu_report_blood, name='received_at_wsu_report_blood'),
    re_path(r"^shipped_to_echo_report/urine/$", reports.shipped_to_echo_report_urine,name='shipped_to_echo_report_urine'),
    re_path(r"^shipped_to_echo_report/blood/$", reports.shipped_to_echo_report_blood,name='shipped_to_echo_report_blood'),

]
