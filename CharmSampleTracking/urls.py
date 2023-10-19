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
from dataview import views as dataviews
from dataview import urls as dataview_urls
from biospecimen import urls as biospecimen_urls

urlpatterns = [
    path('', dataviews.home_page, name='home'),
    path('data/',include(dataview_urls)),
    path('biospecimen/',include(biospecimen_urls)),
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]