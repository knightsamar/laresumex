# Create your views here.
''' import data models '''
from student_info.models import *;

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response;

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
        s, s_created = student.objects.get_or_create(pk=prn); #see the way to unzip a tuple that is returned by a func
        if s_created:
            debugger('No resume found, creating a new one');
        else:
            debugger("Resume found! Using it");
        
        #get all the records and tell us whether they were creatd or retrieved
        tables = (('p','personal'),('sw','software_exposure'),('ex','extraField'),('m','marks'))
        
        #for storing record objects 
        table_data = {'s' : s}

        #whether they were created or retrieved?
        table_data_status = {'s' : s_created}

        for t in tables:
             status,data = eval('%s' % t[1]).objects.get_or_create(primary_table=s); #like calling student.objects.get
             table_data = {'[%s]' % t[0]:data};
             table_status = {'%s' % t[0]:status}; #if False, was retrieved else WAS created
 
             if status:
                 debugger('No %s found, creating a new one' % t[1] );
             else:
                 debugger("%s found! Using it" % t[1]);
             
        
        debugger(table_data);
        debugger(table_data_status);

        c = RequestContext(request,
            {
            'data' : table_data,
            'data_status' : table_status
            });
        
        t = loader.get_template('student_info/form.html');
        t.render(c);
        
        return HttpResponse(t.render(c));

def submit(request):
    '''will accept form submissions and process them -- i don't know why this is seperate from the edit() but i feel it's better FOR NOW'''
    #what is submitted ?
    print request.POST;
    for field, data in request.POST: #it will be a dictionary
        field_name = field.split('_'); #format of the name - tableName FieldName OccurenceId
        print field_name

        if field_name[0] is 'student':
           s = student.object.get_or_create(pk=prn);
           s[field_name[1]] = data;
           s.save();

        elif field_name[0] is 'personal':
           p = personal.object.get_or_create(primary_table=prn);
           #the logic here for updating fields is getting murky and hard-coded

        else:
             """PROBLEMS:
                we need to decide/find/think of a way to deal with MULTIPLE VALUED MULTI LINE DISPLAY wale fields in Edit and Submit views
                Q.1 How do we know that a given value is a new value and NOT a change of existing value ?
                Q.2 How do we name the form widgets (django-slang for html form elements) such that they can preserve their association with the database instances ?
                Q.3 How do we increment properly the ids of such widgets when we Add New, such that they don't corrupt existing rows for other PRNs and still be known that they are NEWER instances of the same class ? == maybe we add a _NEW after them ?
                """

             #if we are retrieving the data
             row = eval("%s" % field_name[0]).objects.get_or_create(primary_table=prn);
             row[field_name[1]] = data;
             row.save();
    pass;

def ajaxRequest(request):
    '''for processing any ajax request for a field data'''
    '''will accept data in XML (ok?) and return data in XML '''
    pass;

def showform(request):
    return render_to_response("student_info/form.html");
