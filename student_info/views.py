# Create your views here.
''' import data models '''
from student_info.models import *;

''' import generator helpers '''
from django.template import Context, loader
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response;
from datetime import datetime

''' import utility functions '''
from student_info.utility import errorMaker, debugger;

def edit(request,prn):
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
        for t,v in tables.iteritems():
            print "=========>>", v  ,"<<======="
            tables[t]=eval(v).objects.filter(primary_table=s)

            for l in tables[t]:
                print l
        tables['s']=s;   
        tables['p']=tables['p'][0]
        tables['sw']=tables['sw'][0];
        
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
        c = RequestContext(request,tables);
        t = loader.get_template('student_info/form.html');
        
        print "dsfasdfasdafsdf"
        return HttpResponse(t.render(c));

def submit(request, prn):
    '''will accept form submissions and process them -- i don't know why this is seperate from the edit() but i feel it's better FOR NOW'''
    #what is submitted ?
    print "I have got files called ", request.FILES;
    for f in request.FILES.values():
            dest="/Users/apoorva/laresumex/STORE/photos/"+ prn+".png"
            print "files to be saved in", dest;
            destination = open(dest, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    
    
    post=request.POST;
    print "========>>>POST<<<========"
    '''for p,v in post.iteritems():
        print p,"..........",v'''
    print "-=======>>> POST", post
    # check for the validity of the prn etc...
    s=student.objects.filter(pk=prn)
    print s, len(s)
    if len(s) is 1:
        print " ======>>> editing original <<<<======="
        s[0].delete()
    
    s= student.objects.create(
        pk=prn,
        fullname=post['fullname'],
        career_objective=post['career_objective'],
        phone_number=post['phone_number']
        )
    
    #post.pop('fullName');
    #post.pop('career_objective');
    #post.pop('phone_number')
    s.save();
    p = personal.objects.get_or_create(primary_table=s)[0];
    table_dict=dict();
    #sw_exposure=dict();
    mvsd=dict();
    l=['marks', 'extracurricular','academic','certification','project','workex']


    for field, data in post.iteritems(): #it will be a dictionary
        field_name = field.split('_'); #format of the name - tableName FieldName OccurenceId
        
        if field == 'csrfmiddlewaretoken':
            continue;

        if len(field_name) is 1: # for student model.
            print "=====>Setting ", field_name[0] , "of student with ",data
            s.__setattr__(field_name[0],data)
            continue;
        if field_name[0] == 'personal':  
            if field_name[2].isdigit() is False:
                index=field_name[1]+'_'+field_name[2];
                print "=====> adding", data , "to attribute", index, "of Personal";
                p.__setattr__(index,data);     
        if field_name[0]=="birthdate":
            date=data.split(',')
            print "=====>DATE<=====",date
            print datetime(int(date[2]),int(date[1]),int(date[0]))
            p.__setattr__("birthdate",datetime(int(date[2]),int(date[1]),int(date[0])));
        
        if str(field_name[0]) in l:# or field_name[0].startswith('ExtraField'): # for multivalued multi display.
           column_dict=dict();
           #if field_name[0].startswith('ExtraField'):

           if field_name[2] == 'X' or field_name[2] =='XII':
               column_dict['course']=field_name[2];
           column_dict[field_name[1]]=data;
           if "title" not in column_dict:
               column_dict['title']=field_name[0]
           index=field_name[0]+'_'+field_name[2];
           if index not in table_dict:
               table_dict[index]=dict()
           table_dict[index].update(column_dict)
           '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=s);
           row[field_name[1]] = data;'''

        elif len(field_name) is 3 and field_name[0] not in l: # for multi-valued sing;e Display
              if field_name[2].isdigit() is False:
                field_name[1]=field_name[1]+'_'+field_name[2]  
              else:
                index=field_name[0]+'_'+field_name[1];
                if index not in mvsd:
                    mvsd[index]=data;
                else:
                   mvsd[index]+=','+data
                                        
    
       
        '''elif field_name[0] == 'swExposure':
            if field_name[1] not in sw_exposure:
                sw_exposure[field_name[1]]=data
            else:
                sw_exposure[field_name[1]]+=','+data'''
                

           #the logic here for updating fields is getting murky and hard-coded

        
            
        """PROBLEMS:
                we need to decide/find/think of a way to deal with MULTIPLE VALUED MULTI LINE DISPLAY wale fields in Edit and Submit views
                Q.1 How do we know that a given value is a new value and NOT a change of existing value ?
                Q.2 How do we name the form widgets (django-slang for html form elements) such that they can preserve their association with the database instances ?
                Q.3 How do we increment properly the ids of such widgets when we Add New, such that they don't corrupt existing rows for other PRNs and still be known that they are NEWER instances of the same class ? == maybe we add a _NEW after them ?
                """

        #if we are retrieving the data
        '''row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=prn);
             row[field_name[1]] = data;
             row.save();'''
             
    p.save();
    print "P saved"
    
    print "=========>>>> The Main list : <=============="    
    print table_dict
    #print "======> s/w Exposure====="
    #print sw_exposure 
    #print "=====>MVSD<======"
    print mvsd
    
    
    # ============>>> MVSD <<<====================
    for table_row, value in mvsd.iteritems():
        if table_row.startswith('Extra'):
            continue;
            print "FO"

        tablerow=table_row.split('_');
        """if tablerow[0] == "personal":
            table=p;
        else:"""    
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
    t=loader.get_template('student_info/submit')
    c=Context(
              {
                  'prn':prn
              }    
            )
    return HttpResponse(t.render(c));


def ajaxRequest(request):
    '''for processing any ajax request for a field data'''
    '''will accept data in XML (ok?) and return data in XML '''
    pass;

def showform(request):
    #prn=request.post['prn'];
    print "sdfsd"
    t=loader.get_template('student_info/form.html')
    c=RequestContext(request,{'flag':'form'});
    
    return HttpResponse(t.render(c));
