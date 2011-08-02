#comment this line when you ARE OUTSIDE SICSR!
#from ldapAuthBackend import authenticate;
from django.http import HttpResponse;
#from django.shortcuts import redirect;
from django.template import RequestContext, loader;
from ldap_login.models import user,group;
from datetime import datetime
from django.core.mail import send_mail
from student_info.utility import our_redirect

from laresumex.settings import ROOT

#from django_auth_ldap.config import LDAPSearch
#ldap_login

def login(request):
    #are we processing login attempt ?
    message = None;
    print request.POST
    if 'username' in request.session:
        return our_redirect('/home');
    if 'username' in request.POST:# and 'password' in request.POST:
        print "== Got username..!!!!"
        if request.POST['username'] == "":
            print"but its empty"
            status=False;
            message="please enter Username"
        else:    
            print "its Not emply...its",request.POST['username']
            print 'processing login attempt';
            try:
                #comment this line when you ARE OUTSIDE SICSR!
                #status = authenticate(request.POST['username'],request.POST['password']);
                #UNCOMMENT the next line when you are outside SICSR!
                status = True;
                print status;
                print 'auth process completed'
            except e as Exception:
                return HttpResponse('Error!!! %s' %  e.message());
            
        if status is True:
            #if successful ldap login
            #update last_login timestamp
            #store encrypted password
            #start session
            request.session['username'] = request.POST['username']; 
            userName=request.session['username']
        	    #check for user existance... and/or add the use in our feedback database..!!
        
            userexists=user.objects.get_or_create(pk=userName)
            userexists[0].save();
		    # this auto gruop assignment takes place by the logic that all students log in from thier PRN's and thier 1st 8 digit of thier PRN represents thier gruop.. to assignm a student to another group we need to do it manually..:) and we need to find out a better way of creating groups..!!! :D
		

		    # to check whether its a student or staff.. :)
            if userName.isdigit() is True:
                print "its a student"
                groupid=userName[0:8];
            else:
                print "its a staff..!"
                groupid='staff'
            print "putting him in group", group;    
            groupexists=group.objects.get_or_create(name=groupid)[0]
            groupexists.save();
            print "groupexists... = ", groupexists
            
            # We will have to think of a better method of doing this..!! eventually
            # for SA and SD ppl 
            """SA=['009','008','020','025','027','030','031','036','046','048','059','069','076','080','090','093','0100','0101'] # add all the SA ppl ka PRN
            if userName[2:8]=="030142": # if they are in msscca
                print "in mscca",userName[2:8]
                if userName[8:11] in SA: # last three digits of PRN
                    print "SA- ", userName[8:11]
                    #sa=group.objects.get_or_create(name='SA')
                    #newuser.groups.add(sa[0])
                else:
                    print "SD", userName[8:11]
                    sd=group.objects.get_or_create(name='SD')
                    #newuser.groups.add(sd])"""
            userexists[0].groups.add(groupexists);
            userexists[0].save();
   
		
            #our_redirect to the index view!
            return our_redirect('/home');
        else: # if status == False
            message = 'Wrong Username/Password';
            print "because status was", status, "hence message is", message;
            print 'redirecting now...';
            

    else: # when we first enter......
   
    # print request.POST['username']
    # print request.POST['password']
      print "nothing is true hence showing the login teplate again"
    #we aren't either procesing a login attempt OR the user had a failed login attempt!

    t = loader.get_template('ldap_login/login.html');
    c = RequestContext (request,
        {
          'message' : message,
          'ROOT' : ROOT,
        });
         
    return HttpResponse(t.render(c));
          
        
    #unsuccessful ldap login
    #wrong username/password!!!

def logout(request):
    #are we actually logged in ?
    if 'username' in request.session:
        print 'logging you out';
		#yes,#then log us out!
        #if len(request.session['unfilled']) is not 0:
            # the person has unfillwd forms
         #   emailid=[request.session['username']+"@sicsr.ac.in"]
         #   print "Sending mail to ",emailid
            #send_mail("unfilled forms", "You have unfilled forms left.. please fill it before the deadline..!!","info@gnunify.in", emailid)
        request.session.flush();
    else:
		#no,
        print 'redirecting to login page to tell you to login first :P';
			#then tell me to login first, using the message if possible 
			#message = "Hey, you need to go in before you can go out :P :P";

    return our_redirect('/ldap_login/');	
