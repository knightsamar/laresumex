## Create your views here.
from student_info.models import student;
from jobposting.forms import JobPostingForm;
from ldap_login.models import *

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect;
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage, get_connection;
from student_info.utility import *; 
from pprint import pprint

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH
from datetime import datetime

def add(request):
    '''
    for adding a new Job Posting 
    '''
    if 'username' not in request.session:
        return HttpResponse('please signup first ;)')

    if request.method == 'POST': # If the form has been submitted...
       form = JobPostingForm(request.POST) # A form bound to the POST
           
       if form.is_valid(): # All validation rules pass
           # Process the data in form.cleaned_data
           # ...
           print form;
           post=request.POST;
           print "=======POST======",post;


           #insert code here to set the values for fields which aren't show in the form but are required to save the instance.
           posted_by = "Samar"; #to be made django-socialauthorized OR ldap_loginized in future

           #now actually save everything
           form.save()
           return HttpResponseRedirect('/common/Thanks/done/') # Redirect after POST
    else:     
      form = JobPostingForm(); # An unbound form
      #print form

    #if the form was invalid OR if there wasn't any submission, just display the form.
    t = loader.get_template('jobposting/form.html')
    c = RequestContext(request, {
                  'form': form,
                  'ROOT':ROOT,
                  })
    return HttpResponse(t.render(c));

