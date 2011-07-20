# Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response, redirect;

''' import vars '''
from laresumex.settings import RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

def search(request):
    return render_to_response('company/search.html')
