#Create your views here.
''' impmrt data models '''
from student_info.models import *;

''' import generator helpers '''
from django.template import Context, loader
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from datetime import datetime

''' import utility functions '''
from student_info.utility import our_redirect,errorMaker, debugger;
from pprint import pprint
from os import path;

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

def edit(request,prn):
    if "username" not in request.session:
       print "no session found"
       return our_redirect("/ldap_login")
    if prn != request.session['username']:
        print "prn", prn, type(prn)
        print "username", request.session['username'],type(request.session['username'])
        return HttpResponse('Please Edit ur own form :@')
    '''The problem with this view :
            We(I) are doing it the old-fashioned way. 
            We(I) are not using the power of Models which allow automatic server-side validation -- i need to read on that.
    '''
        
    #was prn passed and is it numeric really?
    if prn is not None and prn.isdigit() is True:
        #are we authorized to edit this ?
            #do we hv global edit privileges ?

            #kya ye hamara hi resume hai ?

        #do we hv the record ?
        s = student.objects.filter(pk=prn); #see the way to unzip a tuple that is returned by a func
        if len(s) is 0:
            return HttpResponse('This user doesnt exists');
        else:
            s=s[0]
            debugger("Resume found! Using it");
        
        #get all the records and tell us whether they were creatd or retrieved
        tables = {'p':'personal', 'c':'certification','sw':'swExposure','m':'marks','pro':'project','a':'academic','w':'workex','ex':'ExtraField', 'e':'extracurricular'}
        #have moved this to the student_info.models, because all Model info must come from there and tomo if we add a new model, we shouldn't have to come here to provide it's functionality.
        for t,v in tables.iteritems():
            print "=========>>", v  ,"<<======="
            tables[t]=eval(v).objects.filter(primary_table=s)

            for l in tables[t]:
                print l
        tables['s']=s;   
        try:
            tables['p']=tables['p'][0] 
            tables['sw']=tables['sw'][0];
        except Exception as e:    
          pass;
            
        
        '''        
        #for storing record objects 
        table_data = {'s' : s}

        for t in tables:
             status,data = eval('%s' % t[1]).objects.get_or_create(primary_table=s); #like calling student.objects.get
             table_data = {'[%s]' % t[0]:data};
             table_status = {'%s' % t[0]:status}; #if False, was retrieved else WAS created
             if status:
                 debugger('No %s found, creating a new one' % t[1] );
             else:
                 debugger("%s found! Using it" % t[1]);
             
        
        debugger(table_data);
        debugger(table_data_status); '''
        tables['flag']='edit'
        tables['prn']=prn
        tables['ROOT']=ROOT
        c = RequestContext(request,tables);
        t = loader.get_template('student_info/form.html');
        
        print "dsfasdfasdafsdf"
        return HttpResponse(t.render(c));


def submit(request, prn):
    '''processes submissions of NEW forms and also EDIT forms!'''

    if 'username' not in request.session:
        print "no session found"
        return our_redirect('/ldap_login')
    
   #was javascript enabled and everything ok on the client side ???
    if not ('allok' in request.POST and request.POST['allok'] == '1'):
       return HttpResponse("<h2 align='center' style='color: red;'> Hey, you need to enable JavaScript if you want us to help you! </h2>");

    #what is submitted ?
    print "I have got files called ", request.FILES;

    photo_file=RESUME_STORE+"/photos/"+prn+".png";

    if path.exists(photo_file):
        photo_exists = True;  
    else:
        photo_exists = False;

    if not photo_exists and len(request.FILES) is 0:
        return our_redirect('/form')

    #TODO: check whether the photo is a photo or something else ?
    for f in request.FILES.values():
            dest=RESUME_STORE+"/photos/"+prn+".png" #so that things remain soft-coded :P
            print "files to be saved in", dest;
            destination = open(dest, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    
    
    post=request.POST;
    print "========>>>POST<<<========"
    '''for p,v in post.iteritems():
        print p,"..........",v'''
    pprint(post)

    # check for the validity of the prn etc...
    s=student.objects.filter(pk=prn)
    print s, len(s)
    if len(s) is 1:
        print " ======>>> editing original <<<======="
        s[0].delete() #delete to create a new one.
    
    try:

        s = student.objects.create(
            pk=prn,
            fullname=post['fullname'],
            career_objective=post['career_objective'],
            phone_number=post['phone_number']
            )
    
        s.save();
        p = personal.objects.get_or_create(primary_table=s)[0];
        table_dict=dict();
        mvsd=dict();
        extra_fields = dict()
        l = ['marks', 'extracurricular','academic','certification','project','workex'] #list of model names other than personal.

        post_keys = post.keys();
        post_keys.sort();

        for field in post_keys: #it will be a list
            data = post[field]; #get data for this item
            field_name = field.split('_'); #format of the name - tableName_FieldName_OccurenceId
        
            #we are using this long branch of IF and ELIFs because Python doesn't have switch case!!!
            if field == 'csrfmiddlewaretoken':
                continue;
            elif len(field_name) is 1: # for student model
                print "=====>Setting ", field_name[0] , "of student with ",data
                s.__setattr__(field_name[0],data)
                continue;
            elif field_name[0] == 'personal':  
                if field_name[2].isdigit() is False:
                    index=field_name[1]+'_'+field_name[2];
                    print "=====> adding", data , "to attribute", index, "of Personal";
                    p.__setattr__(index,data);     
            if field_name[0]=="birthdate":
                date=data.split(',')
                print "=====>DATE<=====",date
                print datetime(int(date[2]),int(date[1]),int(date[0]))
                p.__setattr__("birthdate",datetime(int(date[2]),int(date[1]),int(date[0])));
            #if it's an ExtraField
            elif 'ExtraField' in field_name[0]:
                #if it's a title
                if field_name[1] == 'title':
                    #create a new object and push it to the ExtraFields dictionary
                    e = ExtraField();
                    e.primary_table = s;
                    e.title = data;
                    extra_fields[''.join(field_name)] = e;
                #if it's a description
                elif field_name[1] == 'desc' or 'year':
                    pass;
                    #take the number at the end of the fieldname
                    #find objects from the ExtraFields dictionary which has this number in it's title or name
                    #for all such objects
                        #does it have the description/year already filled ?
                            #if no,
                                #fill the info.
                                #save
                            #if yes,
                                #go to next object
                        
                         #if still can't find
                            #create a duplicate object of this object but without the description/year.
                            #fill it.
                #elif field_name[0]=="
            if str(field_name[0]) in l:
                column_dict=dict();
                column_dict[field_name[1]]=data;
           
                if "title" not in column_dict:
                    column_dict['title']=field_name[0]
           
                index=field_name[0]+'_'+field_name[2];
           
                if index not in table_dict:
                    table_dict[index]=dict()
           
                    table_dict[index].update(column_dict)
           
            '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=s);
            row[field_name[1]] = data;'''
            if len(field_name) is 3 and field_name[0] not in l: # for multi-valued single Display
              print "!!!!!!!!inside mvsd processing";
              if field_name[2].isdigit() is False:
                field_name[1]=field_name[1]+'_'+field_name[2]  
              else:
                index=field_name[0]+'_'+field_name[1];
                if index not in mvsd:
                    mvsd[index]=data;
                else:
                   mvsd[index]+=','+data
 

            #if we are retrieving the data
            '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=prn);
             row[field_name[1]] = data;
             row.save();'''
             
        p.save();
        print "P saved"
    
        print "=========>>>> The Main list : <=============="    
        pprint(table_dict)
        #print "======> s/w Exposure====="
        #print sw_exposure 
        #print "=====>MVSD<======"
        print mvsd
    except Exception as e:
        return our_redirect('/form')
    
    # ============>>> MVSD <<<====================
    for table_row, value in mvsd.iteritems():
        if table_row.startswith('Extra'):
            continue;
            print "FO"

        tablerow=table_row.split('_');
        if tablerow[0] == "personal":
            table=p;
        else:
            table=eval(tablerow[0]).objects.get_or_create(primary_table=s);
            table=table[0];
        
        print "table-->",table;
        print "we have a column called __%s__" % (tablerow[1]);
        print "value--->",value;
        table.__setattr__(tablerow[1], value);
        table.save();
        print "table value====>>>", table.__getattribute__(tablerow[1])
        print table,".",tablerow[1]," value set to ", table.__getattribute__(tablerow[1]);

    #===========>>> Table Dict <<<=================
    for table, row_values in table_dict.iteritems():
        r=table.split('_')
        print "=======> table ", r[0];
        t=eval(r[0])();
        t.primary_table=s
        print "Creating new row for ", r[0];
        if "desc" in row_values and row_values["desc"] == "":
            print "======>>FALTU FIELD<<======" # for field that just comes in the POST.. will need to fix in the form later.
            continue;
        s.__setattr__(r[0],True);
        for c,d in row_values.iteritems():
            if "monthyear" in c:
                date=d.split(',');
                d=datetime(int(date[2]), int(date[1]), int(date[0]))
                if "end" in c:
                    c="endDate"
                else:
                    c="fromDate"
            t.__setattr__(c,d);
            print r[0],".",c,"======>",d;    
        t.save();    
        print "Saved"
    s.save();
    print "S,saved"
    p.save();
    print "P saved"
    return our_redirect('/student_info/Submitted/done');


def ajaxRequest(request):
    '''for processing any ajax request for a field data'''
    '''will accept data in XML (ok?) and return data in XML '''
    pass;

def showform(request):
    if 'username' not in request.session:
        print "No session"
        return our_redirect('/ldap_login')
    
    #the user shoud not get the form if he already has one.
    try:
        s=student.objects.get(pk=request.session['username'])
        print "student Fornd...", s
    except Exception as e:

        print "student does not exist" 
        prn=request.session['username'];
        print "sdfsd"
    
        t=loader.get_template('student_info/form.html')
        c=RequestContext(request,
            {
                'flag':'form',
                'prn':prn,
                'ROOT':ROOT
            }
            );
    
        return HttpResponse(t.render(c));

    return our_redirect('/student_info/%d/edit' %(int(request.session['username'])))
    return HttpResponse('you arent supposed to see this page. if u see this please contact samar')


def done(request,msg):
  t=loader.get_template('done.html')
  c=Context(
            {
                'msg':msg,
                'ROOT':ROOT
            }
            )
  return HttpResponse(t.render(c)) 
