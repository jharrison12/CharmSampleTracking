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
from django.urls import include,path
from biospecimen import urls as biospecimen_urls
from biospecimen import views as biospecimen_views
from lists import urls as lists_urls
from reports import urls as reports_urls


# app_name='main'
urlpatterns = [
    path('', biospecimen_views.views_caregiver_bio.home_page, name='home'),
    path('biospecimen/',include(biospecimen_urls)),
    path('reports/', include(reports_urls)),
    path('lists/', include(lists_urls)),
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]