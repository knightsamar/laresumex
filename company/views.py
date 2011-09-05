# Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
#from django.shortcuts import render_to_response, redirect;
from company.models import *
from student_info.models import *
from ldap_login.models import *
from datetime import datetime
from student_info.utility import our_redirect,get_done

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH,MEDIA_ROOT

''' import spreadsheet generation module'''
from pyExcelerator import *

#TODO: We have to check the licensing restrictions imposed by it.

def admin_index(request):
     if 'username' not in request.session:
        return our_redirect('/ldap_login/login')
        
     g = groups.objects.get(name='placemnt_committee')

     if user(request.session['username']) not in g:
         return HttpRespose('page not for u');
     t=loader.get_template('company/admin_index.html');
    
     c=RequestContext(request,{
        
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        
        })
     return HttpResponse(t.render(c))


def staff_index(request):
    if 'username' not in request.session:
        return our_redirect('/ldap_login/login')
    
    g = groups.objects.get(name='placemnt_committee')

    if user(request.session['username']) not in g:
         return HttpResponse('page not for u'); 
    com=company.objects.all();
    
    
    t=loader.get_template('company/fetch_students.html');
    
    c=RequestContext(request,{
        'c':com,
        'ROOT':ROOT,
        'MEDIA_URL':MEDIA_URL,
        'list':full_list
        })
    return HttpResponse(t.render(c))


def get_students_name(request):
    if 'username' not in request.session:
        return our_redirect('/ldap_login/login')
    g = groups.objects.get(name='placemnt_committee')

    if user(request.session['username']) not in g:
        return HttpResponse('not for u');
    
    print request.POST; 
    
    try:
        com=company.objects.get(name=request.POST['company_name']);
    except Exception as e:
        return HttpResponse('Select COmpany NAme');
    name_list=list();
    for g in com.students_applied.all():
        s = student.objects.filter(prn=g.prn)
        name_list.extend(s);
 
    print "List of students is ",name_list;
    spreadsheet_name=""
    if  name_list:
        
        #now we will make a spreadsheet of this data.
        wb = Workbook();
        ws0 = wb.add_sheet('Applicants from SICSR');
        #actually, this is going to come from the person who is selecting the list of students.
        fields_to_get=dict()
        for f,v in request.POST.iteritems():
            if f.startswith('criteria'):
                fields_to_get[int(f[9:])]=v
        print "Fields ro get", fields_to_get
        if len(fields_to_get) is 0:
            return HttpResponse('Check Some Fields to be sent to the company')
        #print headings in the spreadsheet
        for f in fields_to_get.keys():
            print "title == ", full_list[f]['display_name'];
            ws0.write(0,f,full_list[f]['display_name']);

        #print data in the spreadsheet
    
        for x in range(len(name_list)):
            print "X is ...", x, "and s is ...",
            # x is the students name list ka index
            s=name_list[x]
            print "for student", s
            for y in fields_to_get.keys(): #hardcoding 4 fields currently
                # y is the fields ka index
                print "fields to get. ....",fields_to_get[y]            
                si=fields_to_get[y].split('_');
                if si[0] == 'student':
                    data = s.__getattribute__(si[1])
                    print "==data===",data    
                elif si[0] == "personal" or si[0] == "swExposure":
                    table= eval(si[0]).objects.get(primary_table=s); 
                    data = str(table.__getattribute__(si[1]))
                elif si[0] == 'workex':
                    data=s.total_workex();
                else:
                    if si[1] == 'graduation':
                        table=marks.get_graduation_course(s)
                        data = str(table)
                    else:    
                        try:
                            table= eval(si[0]).objects.filter(primary_table=s).filter(course=si[1])[0]; 
                            print "we are using table ", table
                            data = str(table.get_percentage());
                        except Exception as e:
                            data  = "-"
                #data = eval("name_list[%d].%s" % (x,fields_to_get[y]));
                print "Writing data %s at %d %d" % (data,x,y);
                ws0.write(x+1,y,data);
    
        spreadsheet_name = "SICSR-%s-applicants.xls" % (com.name.replace(' ','-'));
        wb.save('/tmp/%s' % (spreadsheet_name));
        copy_spreadsheet_command = "cp -v /tmp/%s %s" % (spreadsheet_name,MEDIA_ROOT);
        get_done(copy_spreadsheet_command);

    t = loader.get_template('company/students_list.html')
    c = Context({'company':com,
        'students_applied':name_list,
        'spreadsheet_link':MEDIA_URL+'/'+spreadsheet_name,
        'ROOT':ROOT,
        })
    return HttpResponse(t.render(c))    
    
def got_placed(request):
    if 'username' not in request.session:
        return our_redirect('/ldap_login/login')
    g = groups.objects.get(name='placemnt_committee')

    if user(request.session['username']) not in g:
        return HttpResponse('not for u');
    laced_stu=placement_in.objects.all();
    
    t=loader.get_template('company/got_placed.html');
    c=Context({'PS':placed_stu});
    return HttpResponse(t.render(c))
def search(request):
    t=loader.get_template('company/search.html')
    c=RequestContext(request,{})
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
        return our_redirect('/ldap_login/');
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

    today=datetime.today()
    main_list=list()
    for c in companies:
        c_dict=dict()
        print "processing Companies",c
        c_dict['name']=c.name;
        c_dict['date_of_applying']=c.last_date_of_applying
        c_dict['process']=c.date_of_process
        c_dict['info']=c.eligibilty;
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
                'ROOT':ROOT
                
            });
    return HttpResponse(t.render(c));
def apply(request):
    print request.POST
    #check for the session and our_redirect
    if 'username' not in request.session:
        return our_redirect('/ldap_login/')   
       
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
        
    return our_redirect('/student_info/Saved/done');
