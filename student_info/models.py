from django.db import models
from datetime  import datetime, date; #for django

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"female"))
    prn = models.CharField(max_length=12,unique=True,primary_key=True);
    fullname = models.CharField("First Name", max_length=60, help_text="FULL NAME As on your certificates", blank=False)
    sex=models.CharField(max_length=1,choices=gender);
    email=models.EmailField(max_length=255);
    phone_number=models.CharField(max_length=12);
    backlogs  = models.BooleanField(help_text='do u have backlogs ?');
    yeardrop = models.BooleanField()
    career_objective=models.TextField(blank=False);
    certification=models.BooleanField();
    project=models.BooleanField();
    academic=models.BooleanField();
    extracurricular=models.BooleanField();
    Extra_field=models.BooleanField();
    last_update=models.DateTimeField(auto_now=True);

    def __str__(self):
        return "%s (%s)" % (self.fullname, self.prn);
 

    def total_workex(self):
        '''returns the total workex in months'''
        duration =0
        workex_objs = workex.objects.filter(primary_table=self);
       
        for w in workex_objs:
            duration +=  ((w.endDate - w.fromDate).days)/12; #will return the number of days;

        return duration; 
 
class marks(models.Model):
    primary_table=models.ForeignKey('student');
    course=models.CharField(max_length=30, null=False);
    uni=models.CharField(max_length=100);
    marks=models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True);
    markstype=models.CharField(max_length=10)
    outof=models.IntegerField(null=True, blank=True)
    fromDate=models.DateField(null=True, blank=True);
    
    def __str__(self):
        if self.marks is None:
            return "%s in %s at %s" %(self.markstype,self.course,self.uni)
        return "Obtained %d out of %s in %s at %s" % (self.marks,self.outof,self.course,self.uni)

    class Meta:
        verbose_name_plural = 'Marks of Students';

class personal(models.Model):
     primary_table=models.ForeignKey('student', null=False, unique=True);
     mother_name=models.CharField(max_length=50);
     father_name=models.CharField(max_length=50);
     birthdate=models.DateField(null=True);
     areasofinterest=models.CharField(max_length=100,null=True)
     mother_occupation=models.CharField(max_length=50); 
     father_occupation=models.CharField(max_length=50);
     languages=models.CharField(max_length=200);
     hobbies=models.CharField(max_length=200);
     strength=models.CharField(max_length=200);
     per_address=models.TextField(max_length=200,help_text='Permanent Address');
     corr_address=models.TextField(max_length=200, help_text='Correspondence Address');
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
    
    def __str__(self):
        return "Software Exposure of %s(%s)" % (self.primary_table.fullname, self.primary_table.prn);

    class Meta:
        verbose_name_plural = 'Software Exposures';

class ExtraField(models.Model):
    primary_table=models.ForeignKey('student');
    title=models.CharField(blank=False,max_length=20);
    desc = models.CharField(blank=False,max_length=100);
    fromDate = models.DateField(null=True,blank=True);
    endDate = models.DateField(null=True,blank=True);
    def __str__(self):
        return "Details about %s -%s of %s" % (self.title,self.desc,self.primary_table.fullname);

    class Meta:
        verbose_name_plural = 'ExtraField info about students';

class workex(ExtraField):
    pass;
        
class certification(ExtraField):
    pass;

class project(ExtraField):
    heading=models.CharField(max_length=40 ,blank=True);
    
class academic(ExtraField):
    pass;

class extracurricular(ExtraField):
    pass;




full_list={'student_prn':'Prn', 'student_fullname':'Full Name','student_function_age':'Age','marks_Xth_marks':'10th Marks','marks_XIIth_marks':'12th Marks','marks_B_marks':'Graduation Marks','marks_B_course':'Graduation in','workex_function_workex':'Years of Workex'}
















#for references inside various views
tables = {'p':'personal', 'c':'certification','sw':'swExposure','m':'marks','pro':'project','a':'academic','w':'workex','ex':'ExtraField', 'e':'extracurricular'}

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



