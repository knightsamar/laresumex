## Create your views here.
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
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH,MANAGERS
from datetime import datetime


##### for jobposting #####
def add(request):
    '''
    for adding a new Job Posting 
    
    '''
    if ('username' not in request.session) and (not request.user.is_authenticated()):
        print 'Jobposting using PRN login'
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/')
    else:
        print 'Jobposting using SocialAuth login'
        print request.user.is_authenticated()
        print 'Username: ', request.session.keys()
        if '_auth_user_id' in request.session.keys(): print request.session['_auth_user_id']         
        if '_auth_user_backend' in request.session.keys(): print request.session['_auth_user_backend'] 

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
           postedby.posted_by=request.session['username'] if 'username' in request.session else request.user.username;
           postedby.non_sicsr_poster=True if 'username' not in request.session else False #socialauth-logins don't set this attribute in session
           postedby.save();
           #ref: http://www.quora.com/How-to-save-django-model-form-with-many-to-many-field
           form.save_m2m();

           email = EmailMessage();
           if postedby.non_sicsr_poster: #if non_sicsr_poster
              full_name = request.user.get_full_name() if request.user.get_full_name().strip() != '' else (request.user.username + " from " + request.user.social_auth.values()[0]['provider'])
              if 'provider' in request.user.social_auth.values()[0]:
                  provider = request.user.social_auth.values()[0]['provider']
                  full_name = '%s from %s' % (full_name, provider)
                  #TODO: find a better way, something like model implementation or a f() rather putting things here...
                  profile_link = None
                  if provider == 'facebook':
                      profile_link = 'https://www.facebook.com/%s' % request.user.username
                  #TODO: Find a way to link to google profiles 
                  
           else:
              u = user.objects.get(username = postedby.posted_by)
              full_name = u.fullname if u.fullname.strip()!= '' else u.username

           #TODO: to be implemented when a HTML email solution just like the models is implemented here.
           '''if postedby.non_sicsr_poster and profile_link is not None:
               body = """
               Hi,

               <a href='%s'>%s</a> just posted a new job posting for <b>%s</b> on http://projects.sdrclabs.in/laresumex/jobposting/views/view
               
               Please *approve it* by going to the above link, as soon as possible so that it is available for all the students.
               """  %(profile_link, full_name, postedby.company_name);
           else:'''

           body = """
           Hi,

           <b>%s</b> just posted a new job posting for <b>%s</b> on http://projects.sdrclabs.in/laresumex/jobposting/views/view
           
           Please approve it, by going to the above link, as soon as possible so that it is available for all the students.
           """  %(full_name, postedby.company_name);

           print body
           email.subject = "[LaResume-X]: New job posting";
           email.body = body;
           from django.contrib.auth.models import Group;
           g = Group.objects.get(name = 'placement committee')
           for u in g.user_set.all():
               email.to.append(u.email)
           #add the managers
           for x in MANAGERS:
               email.bcc.append(x[1]);

           print email.to;
           email.send();
           print email.bcc
           return our_redirect('/common/Thanks/done/') # Redirect after POST
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

def view(request,template):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login');
    prn=request.session['username'];
    a="";
    s = user.objects.get(username = prn);
    last_login = request.session['last_login'];
    print "last login =============", last_login;
    empty  = False;
    if 'role' in request.session:
        print "role forn", request.session['role']
        if request.session['role'] == 'admin':
            j = posting.objects.order_by('-posted_on')
            role ="admin"
            if not j:
                empty = True;
        else:
            
            role = "student"
            j = list(posting.objects.filter(status='a').order_by('-posted_on'));
            a = personalised_posting.objects.filter(prn = s ).filter(post__in = j).exclude(is_hidden = True).order_by('-is_interested');
            b = personalised_posting.objects.filter(prn = s ).filter(is_hidden = True);
            print a
            print b
            print j
            for al,bl in map(None,a,b):
                print "SDF",al,bl;
                try:   
                   j.remove(al.post);
                except:
                    pass;
                try:    
                   j.remove(bl.post);
                except:
                    pass;
            if not j and not a:
               empty = True;
    else:
        return HttpResponse('not for u')
    
    t=loader.get_template('jobposting/view.html');
    c=RequestContext(request,{
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        'default_job':j,
        'empty':empty,
        'last_login':last_login,
        'personalized_job':a,
        'message':template,
        'role':role
        })
    return HttpResponse(t.render(c));

def do(request,template):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login');
    if 'role' in request.session:
            role = request.session['role'];
    post = request.POST;
    if len(post) == 1:
        return our_redirect('/home');
    if template == 'views':
     if role == 'student':
      for p,o in post.lists():
            if p == 'csrfmiddlewaretoken':
                continue;
            print p , "=============" , o;
            j = personalised_posting.objects.filter(post__in = o).filter(prn = request.session['username']);
            #print len(j) , len(o);
            print 'j',j;
            print 'o',o;
            for existing_posts in j:
              
              existing_posts.is_interested=( p == 'interested' or p != 'not interested' );
              existing_posts.is_hidden = (p == 'hidden' );
              existing_posts.save();
              print existing_posts.post.id
              o.remove(unicode(existing_posts.post.id));
            print "oooooo==",o; 
            for new_post in o:
                j = personalised_posting(
                    post = posting.objects.get(pk=new_post),
                    is_interested = (p == 'interested' or p != 'not interested' ),
                    is_hidden = (p == 'hidden' ),
                    prn = user.objects.get(username=request.session['username'])
                    )
                j.save();

     elif role == 'admin':
        for p,o in post.lists():
             if p == 'csrfmiddlewaretoken':
                 continue;
             j = posting.objects.filter(pk__in = o);
             j.update(status=p[:1], approved_on = datetime.now());
     return view(request,"DO"); 
    
    
    
    elif template == 'hidden':
        print "post==", post, "post.list",post.lists();
        #i = post.lists().index(u'un-hidden');
        #o = post.lists()[i];
        
        for p,o in post.lists():
             print p 
             print o
             print "======"
             if p == 'un-hidden':    
                 j = personalised_posting.objects.filter(pk__in = o);
                 print j
                 j.update(is_hidden = False);
             print p
             
        return HttpResponse(post.lists());

        
        #get all items by post, i.e job_posting id to the change (interested, hide) theyve made
        #and then update the personalized_post wala table with these changed values. 
        
        
def hidden(request):
    if 'username' not in request.session:
        request.session['redirect'] = request.get_full_path();
        return our_redirect('/ldap_login');
    u = user.objects.get(username = request.session['username']);
    j = personalised_posting.objects.filter(prn = u).filter(is_hidden =True);
    t = loader.get_template('jobposting/view.html');
    c = RequestContext(request,{
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        'hidden_job':j,
        'h':True
        })
    return HttpResponse(t.render(c));

def get_interested_students(request,jp):
    '''this view returns the list of interested students for a jp
       this view is written for calling from the laresumex views 
       unlike the admin code which is written for calling from django admin views

       basically both views call the same model method which has the core functionality of getting interested students.
       both views also use the same template.
    '''
    print 'Getting interested students for jp', jp
    jp = posting.objects.get(pk=jp)
    interested_students = jp.get_interested_students()  
    jpStudents = {'%s : %d students' % (str(jp.company_name),len(interested_students)) : interested_students };

    t = loader.get_template('jobposting/studentsList.html')
    c = Context({'jpStudents':jpStudents})
    return HttpResponse(t.render(c))
