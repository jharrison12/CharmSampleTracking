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
from biospecimen.views import views_caregiver_bio as caregiver_biospecimen
from biospecimen.views import views_child_bio as child_biospecimen

app_name = "biospecimen"
urlpatterns = [
    re_path(r"^$", caregiver_biospecimen.home_page, name='home_page'),
    re_path(r"^error/$", caregiver_biospecimen.error, name='error_page'),
    re_path(r"^entry/$", caregiver_biospecimen.biospecimen_entry, name='biospecimen_entry'),
    re_path(r"^charm_ids/$",caregiver_biospecimen.charm_identifiers, name='charm_identifiers'),
    re_path(r"^charm_ids/(?P<caregiver_charm_id>\w+)/$",caregiver_biospecimen.list_of_bio_ids, name='list_of_bio_ids'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/$", caregiver_biospecimen.caregiver_biospecimen, name='caregiver_biospecimen'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/initial/$", caregiver_biospecimen.caregiver_biospecimen_initial, name='caregiver_biospecimen_initial'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/initial/post/$", caregiver_biospecimen.caregiver_biospecimen_initial_post, name='caregiver_biospecimen_initial_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/kit_sent/post/$", caregiver_biospecimen.caregiver_biospecimen_kit_sent_post, name='caregiver_biospecimen_kit_sent_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/incentive/post/$", caregiver_biospecimen.caregiver_biospecimen_incentive_post, name='caregiver_biospecimen_incentive_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/shipped_choice/post/$", caregiver_biospecimen.caregiver_shipped_choice_post, name='caregiver_shipped_choice_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/shipped_wsu/post/$", caregiver_biospecimen.caregiver_biospecimen_shipped_wsu_post, name='caregiver_biospecimen_shipped_wsu_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/shipped_msu/post/$", caregiver_biospecimen.caregiver_biospecimen_shipped_msu_post, name='caregiver_biospecimen_shipped_msu_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/received_msu/post/$", caregiver_biospecimen.caregiver_biospecimen_received_at_msu_post, name='caregiver_biospecimen_received_at_msu_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/received_wsu/post/$", caregiver_biospecimen.caregiver_biospecimen_received_wsu_post, name='caregiver_biospecimen_received_wsu_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/shipped_echo/post/$", caregiver_biospecimen.caregiver_biospecimen_shipped_echo_post, name='caregiver_biospecimen_shipped_echo_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/processed/post/$", caregiver_biospecimen.caregiver_biospecimen_processed_post, name='caregiver_biospecimen_processed_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/declined/post/$", caregiver_biospecimen.caregiver_biospecimen_declined_post, name='caregiver_biospecimen_declined_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/not_collected/post/$", caregiver_biospecimen.caregiver_biospecimen_not_collected_post, name='caregiver_biospecimen_not_collected_post'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/entry/$", caregiver_biospecimen.caregiver_biospecimen_entry, name='caregiver_biospecimen_entry'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/entry/hairandsaliva/$", caregiver_biospecimen.caregiver_biospecimen_entry_hair_saliva, name='caregiver_biospecimen_entry_hair_saliva'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/entry/blood/$", caregiver_biospecimen.caregiver_biospecimen_entry_blood, name='caregiver_biospecimen_entry_blood'),
    re_path(r"^caregiver/(?P<caregiver_charm_id>\w+)/(?P<caregiver_bio_pk>[\d]+)/post/$", caregiver_biospecimen.caregiver_biospecimen_post, name='caregiver_biospecimen_post'),
    re_path(r"^child/(?P<child_charm_id>\w+)/$", caregiver_biospecimen.child_biospecimen_page, name='child_biospecimen_page'),
    re_path(r"^child/(?P<child_charm_id>\w+)/(?P<child_bio_pk>[\d]+)/initial/$", child_biospecimen.child_biospecimen_page_initial, name='child_biospecimen_page_initial')
]
