# Create your views here.
from student_info.models import student;
from common.forms import ContactForm

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response
from student_info.utility import *; 
from pprint import pprint

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH
from datetime import datetime



def contact(request):
        if request.method == 'POST': # If the form has been submitted...
           form = ContactForm(request.POST) # A form bound to the POST
           
           if form.is_valid(): # All validation rules pass
               # Process the data in form.cleaned_data
               # ...
               print form;

               return HttpResponseRedirect('/common/"successful"/done/') # Redirect after POST
        else:     
           form = ContactForm() # An unbound form
         
        #if the form was invalid OR if there wasn't any submission, just display the form.
        t=loader.get_template('common/contact.html')
        c=RequestContext(request, {
                                'form': form,
                                'ROOT':ROOT,
                                 })
        return HttpResponse(t.render(c));
