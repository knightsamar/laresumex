# Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response, redirect;
from company.models import *
from student_info.models import student
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
    s=student.objects.get(pk=prn);
    companies=company.objects.all();
    print companies
    today=date.today()
    main_list=list()
    for c in companies:
        c_dict=dict()
        print "procesig Compan",c
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
    # check for the session and redirect
    # check for only three entries in POST except for csrfmiddlewaretoken
    # fetch student of ths prn
    #take each company from POST
        #add this student to the list of applied_students
        #save
    return HttpResponse('Saved')
