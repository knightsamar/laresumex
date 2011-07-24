# Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response, redirect;
from company.models import *
from student_info.models import student
from ldap_login.models import *
from datetime import date

''' import vars '''
from laresumex.settings import RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

def search(request):
    c=RequestContext(request,{})
    t=loader.get_template('company/search.html')
    return HttpResponse(t.render(c))

def getResume(request):
    print str(request.POST)
    print "====Now we'l process the post fields..==="
    final_string=""
    for k,v in request.POST.iteritems():
        if k == 'csrfmiddlewaretoken':
            continue
        s=k.split('_')
        #print "==Table name..", s[0],
        #print "Field name ...",s[1]
        if s[2] == "count":
            final_string+="select primary_table from "+ s[0] +" where "+s[1]+" < "+v+"\n";
        else:
            final_string+="select primary_table from "+s[0]+" where "+s[1]+" like %"+v+"% \n";

    print final_string
    return HttpResponse("Please wait till i fetch the resumes...\n\n"+final_string);

def company_list(request):
    if 'username' not in request.session:
        return redirect('/ldap_login/');
    else:
        prn=request.session['username'];
    print prn 
    try:
	       s = student.objects.get(pk=prn)
    except Exception as e:
            output = "<h3>Fill in ur details first</h3>";
            return HttpResponse(output);
    u=user.objects.get(pk=prn)
    companies=list();
    for g in u.groups.all():
        h=company.objects.filter(came_for_group=g)
        for c in h:
            if c not in companies:
                companies.extend(h)

     
    print "companies are ",companies

    today=date.today()
    main_list=list()
    for c in companies:
        c_dict=dict()
        print "processing Companies",c
        c_dict['name']=c.name;
        if c.last_date_of_applying > today:
            c_dict['gone']="";
        else:
            c_dict['gone']="disabled=true";
        m=c.students_applied.all()
        if s in m:
            c_dict['Checked']='Checked=true';
        else:
             c_dict['Checked']="";
        print "the dict", c_dict;
        main_list.append(c_dict)
    print main_list     
    t=loader.get_template('company/company_names')
    c=RequestContext(request,{
                'companies':main_list,
                
            });
    return HttpResponse(t.render(c));
def apply(request):
    print request.POST
    #check for the session and redirect
    if 'username' not in request.session:
        return redirect('/ldap_login/')   
    prn=request.session['username']

    # check for only three entries in POST except for csrfmiddlewaretoken
    if len(request.POST) >4: # onr extra for csrf...
        return HttpResponse('More than Three companies :)')
    # fetch student of ths prn
    
    try:
	       s = student.objects.get(pk=prn)
    except Exception as e:
            output = "<h3>Fill in ur details first</h3>";
            return HttpResponse(output);
    
    # make a list f the companies ths student had applied to pehle
    c=company.objects.filter(students_applied=s)
    #take each company from POST

    for k in request.POST.keys():
         if k == 'csrfmiddlewaretoken':
            continue;
         applied_company=company.objects.get(name=k)
         # if already applied
         if applied_company in c:
             continue;
         else:
            applied_company.students_applied.add(s);
            applied_company.save();           
            #add this student to the list of applied_students
            #save
    # if unchecked.. then remove.
    for k in c:
        if k.name in request.POST.keys():
            continue
        else:
            k.students_applied.remove(s)
            k.save();
    return HttpResponse('Saved')
