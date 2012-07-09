from django.db import models
from datetime  import datetime, date; #for django
from django.db.models.signals import post_save
from datetime import datetime;

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"Female"))
    graduation=['Bsc(H) Computer Science', 'Bsc(IT)']
    prn = models.CharField(max_length=12,unique=True,primary_key=True,verbose_name = 'Permanent Registration Number');
    fullname = models.CharField(max_length=60, verbose_name = 'Full Name',help_text="FULL NAME As on your certificates", blank=False)
    sex = models.CharField(max_length=1, choices=gender, null=False, blank=False, verbose_name='Gender');
    email=models.EmailField(max_length=255, verbose_name='Email Address',);
    phone=models.CharField(max_length=12, blank = True, null = True);
    backlogs  = models.CharField(max_length=1);
    yeardrop = models.CharField(max_length=1);
    career_objective=models.TextField(blank=False, help_text='Keep it short and sweet');
    photo = models.ImageField(upload_to = 'photos', null = False, blank=False, verbose_name='Your Photo',help_text='Your photo which will be displayed in resume and stored in records')
  
    certification=models.BooleanField();
    project=models.BooleanField();
    academic=models.BooleanField();
    extracurricular=models.BooleanField();
    workex=models.BooleanField();
    Extra_field=models.BooleanField();
    last_update=models.DateTimeField(auto_now=True);

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
        
            
class marks(models.Model):
    MARK_TYPES = (('Total','Total Score'),('GPA','GPA'),('Appearing','Appearing'),('Awaiting Result','Awaiting Result'))

    primary_table=models.ForeignKey('student',editable=False);
    course=models.CharField(max_length=30, null=False,verbose_name='Course/Programme');
    uni=models.CharField(max_length=100,verbose_name='University');
    marks=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True,verbose_name='Obtained');
    markstype=models.CharField(max_length=15,choices=MARK_TYPES,blank=False, default=('Total Score'),verbose_name='Marks Type')
    outof=models.DecimalField(max_digits=10,decimal_places=4, blank=True, null=True,verbose_name='Maximum');
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
        verbose_name_plural = 'Marks of Students';

class personal(models.Model):
     primary_table=models.ForeignKey('student', null=False, unique=True);
     mother_name=models.CharField(max_length=50,verbose_name="Mother's Name");
     father_name=models.CharField(max_length=50,verbose_name="Father's Name");
     birthdate=models.DateField(null=False,verbose_name='Your BirthDate');
     areasofinterest=models.CharField(max_length=100,null=True,verbose_name='Areas of Interest');
     mother_occupation=models.CharField(max_length=50,verbose_name="Mother's Occupation"); 
     father_occupation=models.CharField(max_length=50,verbose_name="Father's Occupation");
     languages=models.CharField(max_length=200,verbose_name="Languages Known");
     hobbies=models.CharField(max_length=200);
     strength=models.CharField(max_length=200,verbose_name='Strengths');
     weakness=models.CharField(max_length=200,verbose_name='Weaknesses');
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
        verbose_name_plural = 'Personal Info about students';

class swExposure(models.Model):
    primary_table=models.ForeignKey('student', null=False);
    programming = models.CharField(max_length=100);
    databases = models.CharField(max_length=100)
    OS = models.CharField(max_length=100)
    swPackages = models.CharField(max_length=100)
    webTools = models.CharField(max_length=100)
  
    formname = 'SwExposureForm'

    def __str__(self):
        return "Software Exposure of %s(%s)" % (self.primary_table.fullname, self.primary_table.prn);

    class Meta:
        verbose_name_plural = 'Software Exposures';

class ExtraField(models.Model):
    primary_table=models.ForeignKey('student',editable=False);
    title=models.CharField(blank=False,max_length=20);
    desc = models.TextField(blank=False);
    fromDate = models.DateField(null=True,blank=True);
    endDate = models.DateField(null=True,blank=True);
    def __str__(self):
        return "Details about %s  of %s" % (self.title,self.primary_table.fullname);

    class Meta:
        verbose_name_plural = 'ExtraField info about students';

class workex(ExtraField):
    formname = 'WorkexForm'
    pass;
        
class certification(ExtraField):
    formname = 'CertificationForm'
    pass;

class project(ExtraField):
    formname = 'ProjectForm'
    heading=models.CharField(max_length=40 ,blank=True);
    
class academic(ExtraField):
    formname = 'AcademicAchievementsForm'
    pass;

class extracurricular(ExtraField):
    formname = 'ExtraCurricularForm'
    pass;


# stores company specific details that shd not be stored in the resume
class companySpecific(models.Model):
    Types=(('text','Simple Text'),('radio','Simple yes/No type'),('textarea','a large area'),('special','Type, to render speciallyy -> for experts ;)'))
    datatypes = (('none','none'),('numeric','numbers greater than  0'),('string','Only alphabets and spaces.'));
    
    fieldType=models.CharField(max_length=50,default='text',choices=Types)
    key = models.CharField(max_length=100, help_text="enter a key for internal purposes, WITHOUT SPACES or UNDERSCORE(_)")
    displayText=models.CharField(max_length=100,help_text="The text you want to appear on the form");
    is_mandatory = models.BooleanField(help_text= 'Should this field be mandatory' );
    dataType = models.CharField(max_length = 10, help_text = 'What kinds of imput are allowed???', default = 'none' , choices = datatypes)
    createdOn = models.DateTimeField(auto_now_add = True);

    def __str__(self):
        return self.displayText;


class companySpecificData(models.Model):
    primary_table=models.ForeignKey('student')
    valueOf=models.ForeignKey('companySpecific');
    value=models.CharField(max_length=100,blank=True);
    def __str__(self):
        return "value of %s by %s " %(self.valueOf.displayText, self.primary_table.prn)
   
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
    print "Was a new student instance created ?", kwargs['created']
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

#Whenever a posting is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
for k,model in tables.items():
    post_save.connect(handle_student_updates,sender=eval(model),weak=False,dispatch_uid='studentUpdateSignal');


#In sabko ume actually use karna hai jab hum version treat karenge au
"""
class ExtraTable(models.Model):
    tables = (('p','personal'),('sw','software_exposure'),('ex','extraField'),('m','marks'),('s','student'))
    Column_Type = (('MVOLD','Multi-valued one line display'),
                   ('MVMLD','Multi-valued multiple line display'),
                   ('SVOLD','Single-valued one line display')
                   );

    column_name = models.CharField(max_length=50);
    column_type = models.CharField(max_length=5,choices=Column_Type);
    column_length = models.PositiveIntegerField();
    column_title = models.CharField(max_length=2,choices=tables);

class ExtraTableKaData(models.Model):
    field = models.ForeignKey('ExtraTable');
    data = models.TextField();"""
