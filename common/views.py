# Create your views here.
from student_info.models import student;
from common.forms import ContactForm

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



def contact(request):
        if 'username' not in request.session:
            return HttpResponse('please signup first ;)')
        if request.method == 'POST': # If the form has been submitted...
           form = ContactForm(request.POST) # A form bound to the POST
           
           if form.is_valid(): # All validation rules pass
               # Process the data in form.cleaned_data
               # ...
               print form;
               post=request.POST;
               print "=======POST======",post;

               # sending the email NOW...
               to= ['10030142031@sisr.ac.in',' samar@sicsr.ac.in']
               body=post['message'];
               conn = get_connection();
               email=EmailMessage();
               email.from_email=request.session['username']+'@sicsr.ac.in';
               email.subject='[Laresumex %s]%s %(post["messageType"],post["subject"]';
               email.to=to;
               email.connection=conn;
               email.body=body;
               try:
                email.send();
               except Exception as e:
                print e;
                pass;

               
               
               return HttpResponseRedirect('/common/successful/done/') # Redirect after POST
        else:     
           form = ContactForm() # An unbound form
         
        #if the form was invalid OR if there wasn't any submission, just display the form.
        t=loader.get_template('common/contact.html')
        c=RequestContext(request, {
                                'form': form,
                                'ROOT':ROOT,
                                 })
        return HttpResponse(t.render(c));


def done(request,msg):
  t=loader.get_template('common/done.html')
  c=Context(
            {
                'msg':msg,
                'ROOT':ROOT
            }
            )
  return HttpResponse(t.render(c)) 
