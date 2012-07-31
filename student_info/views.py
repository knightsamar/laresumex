#Create your views here.
''' impmrt data models '''
from student_info.models import *;
from student_info import tables
''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse;
from datetime import datetime
from django.core.exceptions import ValidationError 
from django.contrib import messages

''' import utility functions '''
from student_info.utility import our_redirect,errorMaker, debugger;
from pprint import pprint
from os import path;
from django.utils.encoding import smart_unicode;

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,PHOTO_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH,DEBUG

''' import traceback for debugging '''
if DEBUG is True: #do not import when not needed!
    from sys import exc_info; #for getting traceback
    import traceback; #for printing traceback;

##########################################################################
###################### STUDENT FORM ######################################
##########################################################################

'''
New form(s) implemented using ModelForm and ModelFormset functionality
Named in plural because there are actually multiple forms goin around in this view.
'''

def nayeforms(request,prn):
    #login checker
    if "username" not in request.session:
       print "No session found!"
       request.session['redirect'] = request.get_full_path();
       return our_redirect("/login")
    elif prn != request.session['username']:
       print "prn", prn, type(prn)
       print "username", request.session['username'],type(request.session['username'])
       return HttpResponse('<b>Please edit your own form! :@</b>')

    from student_info.forms import PersonalForm,MarksForm,SwExposureForm,CertificationForm,WorkexForm,AcademicAchievementsForm, ProjectForm, ExtraCurricularForm, StudentForm, AdditionalInfoForm
    from student_info.models import student,personal,swExposure,marks,certification,workex,academic,student,AdditionalInfo, companySpecific, companySpecificData
    from django.forms.models import modelformset_factory

    print "Doing everything for prn", prn
    #for storing the data from the table
    data = {}
    #for storing the factories which generate our formsets
    formset_factories = {}
    #for storing the formsets themselves
    formsets = {}

    invalid_data = False
    s = None;
    
    try:
        s = student.objects.get(pk=prn)
        are_we_editing = True
    except:
        s = student.objects.create(pk=prn)
        are_we_editing = False;

    print "Are we editing", are_we_editing

    if request.method == 'POST': #the form was submitted
        print 'Processing form submission'
        #print "===POST==="
        #print request.POST
 
        try:
            student_data_valid = False
            other_data_valid = False
    
            #formset_factories -- kind of customized factories of forms for each of our models
            formset_factories['marks'] = modelformset_factory(marks,form=MarksForm,extra=0,can_delete=True)
            formset_factories['personal'] = modelformset_factory(personal,form=PersonalForm,extra=0)
            formset_factories['swExposure'] = modelformset_factory(swExposure, form=SwExposureForm, extra=0)
            formset_factories['certification'] = modelformset_factory(certification, form=CertificationForm, extra=0,can_delete=True)
            formset_factories['workex'] = modelformset_factory(workex, form=WorkexForm, extra=0,can_delete=True)
            formset_factories['academic'] = modelformset_factory(academic, form=AcademicAchievementsForm, extra=0,can_delete=True)
            formset_factories['extracurricular'] = modelformset_factory(extracurricular, form=ExtraCurricularForm, extra=0,can_delete=True)
            formset_factories['project'] = modelformset_factory(project, form=ProjectForm, extra=0,can_delete=True)
            formset_factories['additionalInfo'] = modelformset_factory(AdditionalInfo, form=AdditionalInfoForm, extra=0,can_delete=True)

            #generate a formset -- collection of forms for editing/creating new data
            formsets['marks'] = formset_factories['marks'](request.POST,prefix='marks')
            formsets['personal'] = formset_factories['personal'](request.POST,prefix='personal')
            formsets['swExposure'] = formset_factories['swExposure'](request.POST,prefix='swExposure')
            formsets['certification'] = formset_factories['certification'](request.POST,prefix='certification')
            formsets['workex'] = formset_factories['workex'](request.POST,prefix='workex')
            formsets['academic'] = formset_factories['academic'](request.POST,prefix='academic')
            formsets['extracurricular'] = formset_factories['extracurricular'](request.POST,prefix='extracurricular')
            formsets['project'] = formset_factories['project'](request.POST,prefix='project')
            formsets['additionalInfo'] = formset_factories['additionalInfo'](request.POST,prefix='additionalInfo')

            sf = StudentForm(request.POST,request.FILES,prefix='student',instance=s)
            
            print 'Starting to save data'
            print 'Processing Company Specific info'
            #WORST way of identifiying Company Specific fields for processing -- but can't find a better way, for now.
            for field,value in request.POST.lists():
                field_name = field.split('_')
                print "Field ",field
                print "Value ",value
                if (field_name[0] == 'companySpecific'):
                    try:
                        print 'On',field, 'and Data',value
                        cs = companySpecific.objects.get(key=field_name[1])    
                        print "\n\n\nCOMPANY SPECIFIC...!!!!!!...", value, type(value);
                        
                        final_value = str(value[0]);
                        for v in value[1:]:
                            final_value += ',' + v
                        
                        csd, created_or_found = companySpecificData.objects.get_or_create(valueOf=cs,primary_table=s)
                        csd.value = value
                        csd.save()
                        print 'Saving Company Specific Data'

                        other_data_valid = True;
                    except Exception as e:
                        print "==================="
                        print "Error with Company data :",
                        print e
                        other_data_valid = False;
                        #Add the error message to be displayed in the template
                        messages.error(request, "<b>Company Specific Info :</b> %s" % e)
                        #raise exception so that we can go back to displaying the form
                        raise Exception;

            print 'Processing student data',
            student_data_valid = sf.is_valid()

            if student_data_valid:
                print 'Saved all submitted data for Student Basic info'
                sf.save()
            else:
                print "==================="
                print "Error with Student data :",
                print sf.errors;
                #Add the error message to be displayed in the template
                messages.error(request, "<b>Basic Information: </b>%s" % sf.errors); 
                #raise exception so that we can go back to displaying the form
                raise Exception;

            print 'Student data validity status : %s' % student_data_valid
            for f in formsets:
                #formsets[f].clean()
                print 'Processing ',f
                other_data_valid = formsets[f].is_valid()
                if other_data_valid:
                    instances = formsets[f].save(commit=False)
                    for i in instances:
                        i.primary_table = s
                        i.save()
                        print 'Saved all submitted data for ',f
                else:
                    #Error!!
                    print "==================="
                    print "Error with %s is :" % (f)
                    print formsets[f].errors;
                    print 'Other data validity status is : %s' % other_data_valid 
                    #Add the error message to be displayed in the template
                    messages.error(request, "<b>%s :</b> %s " % (f.title(),formsets[f].errors)); 
                    #raise exception so that we can go back to displaying the form
                    raise Exception;
        except:
            if (not student_data_valid) and (not are_we_editing): #we were trying to save a NEW student's data and encountered problem
                print 'Student data is invalid and we are creating new record',
                s.delete()
            elif (not student_data_valid) and (are_we_editing): #we were trying to save a OLD student's data and encountered errors
                print 'Student data is invalid and we are editing',
                pass #the data wasn't actually saved because of django's mechanisms
            elif (not other_data_valid) and (not are_we_editing):
                print "Figure out what to do in case tehre are errors in saving NEW data for a student in various models"
                pass
            elif (not other_data_valid) and (are_we_editing):
                print 'Other data is invalid and we are editing existing details'
                pass #the data wasn't actually saved because of django's mechanisms

        if student_data_valid and other_data_valid:
            return our_redirect('/common/Submitted/done');
        else:
            #Company Specific fields -- special thingys ;) 
    	    #These provide dynamic fields in the form which can be added in the form by the placement team.
            #existing data for company specific fields
            data['companySpecificData'] = companySpecificData.objects.filter(primary_table=s).order_by('valueOf')
            already_filled_list = data['companySpecificData'].values_list('valueOf')

            #provide for new fields to be displayed to user
            #here we select only those fields which haven't been filled by the user as obtained in the above list.
            #basically this is a query which says -->
            #"Give me all Company Specific fields excluding those whose values have been filled by the user and order them by their displayText"

            data['companySpecificFields'] = companySpecific.objects.all().exclude(fieldType='special').exclude(id__in=already_filled_list).order_by('displayText') 

            print "Invalid data! Returning form for editing";
    else: #new form is being displayed
        print 'Displaying new/edit form'

        data['marks'] = marks.objects.filter(primary_table=prn)
        if data['marks'].count() == 0: #no existing data for this student
           print "No existing marks data found for this student"
           formset_factories['marks'] = modelformset_factory(marks,form=MarksForm,exclude=('primary_table'),extra=3, can_delete=True)
           formsets['marks'] = formset_factories['marks'](prefix='marks',queryset = data['marks'])
        else:
           formset_factories['marks'] = modelformset_factory(marks,form=MarksForm,extra=0,can_delete=True)
           formsets['marks'] = formset_factories['marks'](prefix='marks',queryset = data['marks'])

        data['personal'] = personal.objects.filter(primary_table=prn)
        if data['personal'].count() == 0:
           print "No existing personal data found for this student"
           formset_factories['personal'] = modelformset_factory(personal,form=PersonalForm,extra=1)
           formsets['personal'] = formset_factories['personal'](prefix='personal',queryset = data['personal'])
        else:
           formset_factories['personal'] = modelformset_factory(personal,form=PersonalForm,extra=0)
           formsets['personal'] = formset_factories['personal'](prefix='personal',queryset = data['personal'])
        
        data['swExposure'] = swExposure.objects.filter(primary_table=prn)
        if data['swExposure'].count() == 0:
           print "No existing software exposure data found for this student"
           formset_factories['swExposure'] = modelformset_factory(swExposure,form=SwExposureForm,extra=1)
           formsets['swExposure'] = formset_factories['swExposure'](prefix='swExposure',queryset = data['swExposure'])
        else:
           formset_factories['swExposure'] = modelformset_factory(swExposure,form=SwExposureForm,extra=0)
           formsets['swExposure'] = formset_factories['swExposure'](prefix='swExposure',queryset = data['swExposure'])
        
        data['certification'] = certification.objects.filter(primary_table=prn)
        if data['certification'].count() == 0:
           print "No existing certification data found for this student"
           formset_factories['certification'] = modelformset_factory(certification,form=CertificationForm,extra=1,can_delete=True)
           formsets['certification'] = formset_factories['certification'](prefix='certification',queryset=data['certification'])
        else:
           formset_factories['certification'] = modelformset_factory(certification,form=CertificationForm,extra=0,can_delete=True)
           formsets['certification'] = formset_factories['certification'](prefix='certification',queryset = data['certification'])

        data['workex'] = workex.objects.filter(primary_table=prn)
        if data['workex'].count() == 0:
           print "No existing workex data found for this student"
           formset_factories['workex'] = modelformset_factory(workex, form=WorkexForm, extra=1,can_delete=True)
           formsets['workex'] = formset_factories['workex'](prefix='workex',queryset=data['workex'])
        else:
           formset_factories['workex'] = modelformset_factory(workex, form=WorkexForm, extra=0,can_delete=True)
           formsets['workex'] = formset_factories['workex'](prefix='workex',queryset = data['workex'])

        data['academic'] = academic.objects.filter(primary_table=prn)
        if data['academic'].count() == 0:
           print "No existing academic data found for this student"
           formset_factories['academic'] = modelformset_factory(academic, form=AcademicAchievementsForm, extra=1,can_delete=True)
           formsets['academic'] = formset_factories['academic'](prefix='academic',queryset=data['academic'])
        else: #existing data was found for this student 
           formset_factories['academic'] = modelformset_factory(academic, form=AcademicAchievementsForm, extra=0,can_delete=True)
           formsets['academic'] = formset_factories['academic'](prefix='academic',queryset=data['academic'])

        data['project'] = project.objects.filter(primary_table=prn)
        if data['project'].count() == 0:
           print "No existing project data found for this student"
           formset_factories['project'] = modelformset_factory(project, form=ProjectForm, extra=1,can_delete=True)
           formsets['project'] = formset_factories['project'](prefix='project',queryset=data['project'])
        else: #existing data was found for this student 
           formset_factories['project'] = modelformset_factory(project, form=ProjectForm, extra=0,can_delete=True)
           formsets['project'] = formset_factories['project'](prefix='project',queryset=data['project'])

        data['extracurricular'] = extracurricular.objects.filter(primary_table=prn)
        if data['extracurricular'].count() == 0:
           print "No existing extracurricular data found for this student"
           formset_factories['extracurricular'] = modelformset_factory(extracurricular, form=ExtraCurricularForm, extra=1,can_delete=True)
           formsets['extracurricular'] = formset_factories['extracurricular'](prefix='extracurricular',queryset=data['extracurricular'])
        else: #existing data was found for this student 
           formset_factories['extracurricular'] = modelformset_factory(extracurricular, form=ExtraCurricularForm, extra=0,can_delete=True)
           formsets['extracurricular'] = formset_factories['extracurricular'](prefix='extracurricular',queryset=data['extracurricular'])

        data['additionalInfo'] = AdditionalInfo.objects.filter(primary_table=prn)
        if data['additionalInfo'].count() == 0:
           print "No existing additionalInfo data found for this student"
           formset_factories['additionalInfo'] = modelformset_factory(AdditionalInfo, form=AdditionalInfoForm, extra=1,can_delete=True)
           formsets['additionalInfo'] = formset_factories['additionalInfo'](prefix='additionalInfo',queryset=data['additionalInfo'])
        else: #existing data was found for this student 
           formset_factories['additionalInfo'] = modelformset_factory(AdditionalInfo, form=AdditionalInfoForm, extra=0,can_delete=True)
           formsets['additionalInfo'] = formset_factories['additionalInfo'](prefix='additionalInfo',queryset=data['additionalInfo'])

        #Company Specific fields -- special thingys ;) 
	    #These provide dynamic fields in the form which can be added in the form by the placement team.
        #existing data for company specific fields
        data['companySpecificData'] = companySpecificData.objects.filter(primary_table=s).order_by('valueOf')
        already_filled_list = data['companySpecificData'].values_list('valueOf')

        #provide for new fields to be displayed to user
        #here we select only those fields which haven't been filled by the user as obtained in the above list.
        #basically this is a query which says -->
        #"Give me all Company Specific fields excluding those whose values have been filled by the user and order them by their displayText"

        data['companySpecificFields'] = companySpecific.objects.all().exclude(fieldType='special').exclude(id__in=already_filled_list).order_by('displayText') 
        
        #Student Data 
        data['student'] = s
        sf = StudentForm(prefix='student',instance=data['student'])

    t = loader.get_template('student_info/nayeforms.html')
    context = {
        'prn' : prn,
        'marks_formset' : formsets['marks'],
        'personal_formset' : formsets['personal'],
        'swExposure_formset' : formsets['swExposure'],
        'certification_formset' : formsets['certification'],
        'workex_formset': formsets['workex'],
        'academic_formset' : formsets['academic'],
        'project_formset' : formsets['project'],
        'extracurricular_formset' : formsets['extracurricular'],
        'additionalInfo_formset':formsets['additionalInfo'],
        'student_form' : sf,
        's' : s, #student object
        'ROOT' : ROOT,
        'companySpecificData': data['companySpecificData'],
        'companySpecificFields': data['companySpecificFields'],
        }
    
    c = RequestContext(request,context)

    return HttpResponse(t.render(c))
