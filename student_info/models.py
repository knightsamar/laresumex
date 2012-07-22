from django.db import models
from datetime  import datetime, date; #for django
from django.db.models.signals import post_save
from datetime import datetime;
from laresumex.settings import PHOTO_STORE

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"Female"))
    graduation=['Bsc(H) Computer Science', 'Bsc(IT)']
    prn = models.CharField(max_length=12,unique=True,primary_key=True,verbose_name = 'Permanent Registration Number');
    fullname = models.CharField(max_length=60, verbose_name = 'Full Name',help_text="FULL NAME as on your certificates", blank=False)
    sex=models.CharField(max_length=1,choices=gender, null=False, blank=False, verbose_name='Gender');
    email=models.EmailField(max_length=255, verbose_name='Email Address',);
    phone=models.CharField(max_length=12, blank = True, null = True);
    career_objective=models.TextField(blank=False, help_text='Keep it short and sweet');
    photo = models.ImageField(upload_to = PHOTO_STORE, null = False, blank=False, verbose_name='Your Photo',help_text='Your photo which will be displayed in resume and stored in records')
    
    #boolean fields
    certification=models.BooleanField();
    project=models.BooleanField();
    academic=models.BooleanField();
    extracurricular=models.BooleanField();
    workex=models.BooleanField();
    Extra_field=models.BooleanField();
    
    #when was this record and corresponding information for the student in various tables last updated on?
    #this field is also updated by the handle_student_updates signal handler 
    last_update=models.DateTimeField(auto_now=True,verbose_name='Last Updated on');
    formname = 'StudentForm'

    def __str__(self):
        return "%s (%s)" % (self.fullname, self.prn);
 

    def total_workex(self):
        '''returns the total workex in months'''
        duration =0
        workex_objs = workex.objects.filter(primary_table=self);
       
        for w in workex_objs:
            duration +=  ((w.endDate - w.fromDate).days)/12; #will return the number of days;

        return duration; 

    def get_resume_path(self):
        from generate_resume.models import resume
        try :
            r = resume.objects.get(prn = self.prn);
            return r.get_pdf_path()
        except resume.DoesNotExist as e:
            return None
    
    class Meta:
        verbose_name_plural = "Student's Information"
    
class marks(models.Model):
    MARK_TYPES = (('Total','Total Score'),('GPA','GPA'),('Appearing','Appearing'),('Awaiting Result','Awaiting Result'))

    primary_table=models.ForeignKey('student',editable=False);
    course=models.CharField(max_length=30, null=False,verbose_name='Course/Programme');
    uni=models.CharField(max_length=100,verbose_name='University/Board');
    marks=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True,verbose_name='Obtained Score/GPA');
    markstype=models.CharField(max_length=15,choices=MARK_TYPES,blank=False, default=('Total Score'),verbose_name='Marks Type')
    outof=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True,verbose_name='Maximum Score/GPA');
    fromDate=models.DateField(null=True, blank=True,verbose_name='Date of Completion',help_text='Enter the Month & Year you completed/will complete this Course.');    

    formname = 'MarksForm'

    def __str__(self):
        if self.marks is None:
            return "%s in %s at %s" %(self.markstype,self.course,self.uni)
        return "%s Obtained %s out of %s in %s at %s" % (self.primary_table,self.marks,self.outof,self.course,self.uni)


    def get_percentage(self):
        '''returns percentage on good data and returns false on bad data or exceptions'''
        try:
            percentage = (self.marks / self.outof) * 100;
            return round(percentage,2);
        except Exception as e:
            print "Can't get percentage because : ",e;
            return False;

    '''Using syntactic sugar :D ref: http://docs.python.org/library/functions.html#staticmethod 
    SADLY: this staticmethod thingy doesn't work with django. So we can't use it.
    '''
    @staticmethod
    def get_graduation_course(prn):
        '''get all marks objects who are graduation = (not 10,12) AND (not starting with M which is for Masters) and IS belonging to the PRN'''
        ms = marks.objects.filter(course__istartswith='B').filter(primary_table=prn);
        try:
            return ms[0];
        except Exception as e:
            return 'not mentioned';
    class Meta:
        verbose_name_plural = 'Marks + Qualification Info of Students';

class personal(models.Model):
     primary_table=models.ForeignKey('student', null=False, unique=True);
     mother_name=models.CharField(max_length=50,verbose_name="Mother's Name");
     father_name=models.CharField(max_length=50,verbose_name="Father's Name");
     birthdate=models.DateField(null=False,verbose_name='Your BirthDate');
     areasofinterest=models.CharField(max_length=100,null=True,verbose_name='Areas of Interest', help_text='Enter areas of interest seperated by commas');
     mother_occupation=models.CharField(max_length=50,verbose_name="Mother's Occupation");
     father_occupation=models.CharField(max_length=50,verbose_name="Father's Occupation");
     languages=models.CharField(max_length=200,verbose_name="Languages Known",help_text='Enter languages seperated by commas');
     hobbies=models.CharField(max_length=200,help_text='Enter hobbies seperated by commas');
     strength=models.CharField(max_length=200,verbose_name='Strengths',help_text='Enter strengths seperated by commas');
     weakness=models.CharField(max_length=200,verbose_name='Weaknesses',help_text='Enter weaknesses seperated by commas');
     per_address=models.TextField(max_length=200,verbose_name='Permanent Address');
     corr_address=models.TextField(max_length=200, verbose_name='Correspondence Address');
     
     formname = 'PersonalForm'

     def get_age(self):
        '''returns age'''
        age=date.today()-self.birthdate
        return (age.days /365)
     def __str__(self):
        return "Personal details about %s (%s)" % (self.primary_table.fullname, self.primary_table.prn);

     class Meta:
        verbose_name_plural = 'Personal Info of Students';

class swExposure(models.Model):
    primary_table=models.ForeignKey('student', null=False);
    programming = models.CharField(max_length=100,verbose_name='Programming Languages',help_text='Enter Programming Languages that you know seperated by commas');
    databases = models.CharField(max_length=100,verbose_name='Databases',help_text='Enter Databases that you know seperated by commas')
    OS = models.CharField(max_length=100,verbose_name='Operating Systems',help_text='Enter Operating Systems that you know seperated by commas')
    swPackages = models.CharField(max_length=100,verbose_name='Software Packages',help_text='Enter Software Packages that you know seperated by commas')
    webTools = models.CharField(max_length=100,verbose_name='Web Tools', help_text='Enter Web Tools seperated by commas')
  
    formname = 'SwExposureForm'

    def __str__(self):
        return "Software Exposure of %s(%s)" % (self.primary_table.fullname, self.primary_table.prn);

    class Meta:
        verbose_name_plural = 'Software Exposure info of students';

class ExtraField(models.Model):
    primary_table=models.ForeignKey('student',editable=False);
    title=models.CharField(blank=False,max_length=20);
    desc = models.TextField(blank=False,verbose_name='Description',help_text='Describe it in brief.');
    fromDate = models.DateField(null=True,blank=True, verbose_name='From Date',help_text='Enter the Month and Year when you started this');
    endDate = models.DateField(null=True,blank=True, verbose_name='To Date',help_text='Enter the Month and Year when you completed/will complete this');

    formname = 'ExtraFieldForm'

    def __str__(self):
        return "Details about %s  of %s" % (self.title,self.primary_table.fullname);
    
    class Meta:
        verbose_name_plural = 'Uncategorized Extra Info of Students';

class workex(ExtraField):
    
    formname = 'WorkexForm'
    
    class Meta:
        verbose_name_plural = "Work Experience Info of Students"

class certification(ExtraField):
    formname = 'CertificationForm'
    
    class Meta:
        verbose_name_plural = "Certification Info of students"

class project(ExtraField):
    heading=models.CharField(max_length=40 ,blank=True);
    
    formname = 'ProjectForm'
    class Meta:
        verbose_name_plural = 'Project Info of Students'

class academic(ExtraField):
    formname = 'AcademicAchievementsForm'

    class Meta:
        verbose_name_plural = 'Academic Info of Student'

class extracurricular(ExtraField):
    formname = 'ExtraCurricularForm'
    class Meta:
        verbose_name_plural = 'Extra Curricular Infor of Students'

# stores company specific details that shd not be stored in the resume
class companySpecific(models.Model):
    Types=(('text','Simple Text'),('radio','Simple yes/No type'),('textarea','a large area'),('special','Type, to render speciallyy -> for experts ;)'))
    datatypes = (('none','none'),('numeric','numbers greater than  0'),('string','Only letters from the alphabet and spaces.'));
    
    fieldType=models.CharField(max_length=50,default='text',choices=Types, help_text='Field Type', verbose_name='Type of Field')
    key = models.CharField(max_length=100, help_text="Enter a key for internal purposes, WITHOUT SPACES or UNDERSCORE(_)", verbose_name='Internal Field Name')
    displayText = models.CharField(max_length=100, help_text="What name should be displayed to the student filling details?", verbose_name='Field label displayed to Student');
    is_mandatory = models.BooleanField(help_text= 'Should this field be made mandatory?',verbose_name='Is mandatory?');
    dataType = models.CharField(max_length = 10, help_text = 'What kinds of inputs are allowed?', default = 'none' , choices = datatypes, verbose_name='Type of Data allowed')
    createdOn = models.DateTimeField(auto_now_add = True, verbose_name='Field was created on', editable=False);

    def __str__(self):
        return self.displayText;

    class Meta:
        verbose_name_plural = 'Company Specific Fields'
        verbose_name = 'Company Specific Field'

class companySpecificData(models.Model):
    primary_table=models.ForeignKey('student',verbose_name='Info filled by')
    valueOf=models.ForeignKey('companySpecific',verbose_name='Value for field');
    value=models.CharField(max_length=100,blank=True, verbose_name='Value filled');

    def __str__(self):
        return "Value for '%s' by '%s' " %(self.valueOf.displayText, self.primary_table.prn)
   
    class Meta:
        verbose_name_plural = "Data for Company Specific Fields"
        verbose_name = 'Data for Company Specific Field'

#for references inside various views
tables = {'p':'personal', 'c':'certification','sw':'swExposure','m':'marks','pro':'project','a':'academic','w':'workex','ex':'ExtraField', 'e':'extracurricular'}

def handle_student_updates(sender, **kwargs):
    '''Signal handler whenever any of a student related data is modified and saved
       Refer: http://localhost/docs/django-docs/ref/signals.html#django.db.models.signals.post_save
    '''
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print "A signal was sent by ", sender
    print 
    print "The instance which forced the signal to sent was ", kwargs['instance']
    print 
    #would be applicable if we would be processing post_save
    print "Was a new instance created ?", kwargs['created']
    try:
       if kwargs['instance'].primary_table:
           s = kwargs['instance'].primary_table;
           print 'Found the student whose data was last modified on %s ' % (s.last_update)
           s.last_update = datetime.now();
           s.save();
           print 'Changed last modified to %s ' % (s.last_update)
       else:
           print "Can't get prn";
    except Exception as e:
        print "Exception %s occured" % e;
    print "++++++++++++++++++++++++++++++++++++++++++++"

#Whenever any student related data is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
for k,model in tables.items():
    post_save.connect(handle_student_updates,sender=eval(model),weak=False,dispatch_uid='studentUpdateSignal');

