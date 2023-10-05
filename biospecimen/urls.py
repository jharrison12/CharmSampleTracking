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
from biospecimen import views as biospecimen_views

app_name = "biospecimen"
urlpatterns = [
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/$", biospecimen_views.caregiver_biospecimen, name='caregiver_biospecimen'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/entry/$", biospecimen_views.caregiver_biospecimen_entry, name='caregiver_biospecimen_entry'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<biospecimen>[\w\ ]+)/(?P<collection_num>[\w]+)/history/$", biospecimen_views.caregiver_biospecimen_item, name='caregiver_biospecimen_item'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/initial/$",biospecimen_views.caregiver_biospecimen_initial, name='caregiver_biospecimen_initial'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/initial/post/$",biospecimen_views.caregiver_biospecimen_initial_post, name='caregiver_biospecimen_initial_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/shipped_choice/post/$",biospecimen_views.caregiver_shipped_choice_post, name='caregiver_shipped_choice_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/entry/$", biospecimen_views.caregiver_biospecimen_entry, name='caregiver_biospecimen_entry'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/post/$", biospecimen_views.caregiver_biospecimen_post, name='caregiver_biospecimen_post'),
    re_path(r"^child/(?P<child_charm_id>\w+)/$", biospecimen_views.child_biospecimen_page,name='child_biospecimen_page')
]
