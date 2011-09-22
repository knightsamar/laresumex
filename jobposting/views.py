## Create your views here.
from student_info.models import student;
from jobposting.forms import JobPostingForm;
from jobposting.models import *
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


##### for jobposting #####
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

           #now actually save everything
           postedby=form.save(commit=False);
           postedby.posted_by=request.session['username'];
           postedby.save();

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

#####  view  #####

def view(request):
    if 'username' not in request.session:
        return our_redirect('/ldap_login');
    prn=request.session['username'];
    if 'role' in request.session:
        print "role fornf", request.session['role']
        if request.session['role'] == 'admin':
            j = posting.objects.filter(status='p')
            role ="admin"
        else:
            role = "student"
            j = posting.objects.filter(status='a');
    else:
        return HttpResponse('not for u')
    t=loader.get_template('jobposting/view.html');
    c=RequestContext(request,{
        'ROOT':ROOT,
        'job':j,
        'role':role
        })
    return HttpResponse(t.render(c));

def do(request):
    if 'username' not in request.session:
        return our_redirect('/ldap_login');
    post = request.POST;
    for p,o in post.iteritems():
        print p , "=============" , o;
    return HttpResponse('hi') 
    #get all items by post, i.e job_posting id to the change (interested, hide) theyve made
    #and then update the personalized_post wala table with these changed values. 
        
        


