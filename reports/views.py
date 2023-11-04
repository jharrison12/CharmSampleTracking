import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
@login_required
def home_page(request):
    return render(request=request,template_name='reports/home.html')