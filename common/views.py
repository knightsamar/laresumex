# Create your views here.
from student_info.models import student;
from common.forms import ContactForm
from ldap_login.models import *

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect;
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage;
from student_info.utility import *; 
from pprint import pprint

''' import vars '''
from laresumex.settings import MANAGERS,ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH
from datetime import datetime


def index(request):
    if 'username' not in request.session:
        print "from home to login as No session"
        return our_redirect('/ldap_login')
    # see whether user has logged in...
    # if yes, see whether the user has already filled resume, then remove the create button.
    # if no.. then remove the edit and the viw resume button.
    prn = request.session['username']
    print "hamra prnwa hai ",prn;
    u=user.objects.get(username=prn);
    g=group.objects.get(name='placement committee')
    placement_staff_student=[0,0,0];
    if u in g.user_set.all():
        print 'placement_committe'
        request.session['role']='admin'
        placement_staff_student[0]=1;
    elif prn.isdigit():
        print "student"
        request.session['role']='student'
        placement_staff_student[2]=1;
    else:
        print "staff"
        placement_staff_student[1]=1;

    print "found prn"
    try:
            s=student.objects.get(pk=prn);
            #Form already exists
            create_form=False
    except Exception as e:
            #it means there is no entry
            create_form=True;
       
    t=loader.get_template('common/index.html')
    
    c=Context({
            'prn':request.session['username'],
            'create_form':create_form,
            'p_s_st':placement_staff_student,
            'MEDIA_URL' : MEDIA_URL,
            'ROOT':ROOT
             }
            );
    return HttpResponse(t.render(c));

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
               to = []
               for m in MANAGERS:
                   to.append(list(m)[1])
               
               email=EmailMessage();
               for f in request.FILES.values() :
                   dest=RESUME_STORE+"/error/"+request.session['username']+".png";
                   destination = open(dest,'wb+')
                   for c in f.chunks():
                       destination.write(c)
                   destination.close()
                   email.attach_file(dest); 
               
               body=post['message'];
               email.from_email=request.session['username']+'@sicsr.ac.in';
               email.subject='[Laresumex'+ post['messageType']+']'+ post['subject'];
               email.to=to;
               email.body=body;
               email.send();

               
               
               return our_redirect("/common/Thank you/done") # Redirect after POST
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
