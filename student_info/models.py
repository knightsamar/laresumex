from django.db import models

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"female"))
    
    prn = models.CharField(max_length=12,unique=True,primary_key=True);
    fullname = models.CharField("First Name", max_length=60, help_text="FULL NAME As on your certificates", blank=False)
    sex=models.CharField(max_length=1,choices=gender);
    email=models.EmailField(max_length=75);
    phone_number=models.PositiveIntegerField(max_length=10);
    career_objective=models.TextField(blank=False);
    certification=models.BooleanField();
    Projects=models.BooleanField();
    academic_qualifications=models.BooleanField();
    Extra_curricular=models.BooleanField();
    Extra_field=models.BooleanField();
   
    def __str__(self):
        return " Resume details of %s(%s)" % (self.fullname, self.prn);
 
class marks(models.Model):
    primary_table=models.ForeignKey('student');
    course=models.CharField(max_length=30, null=False);
    uni=models.CharField(max_length=100);
    marks=models.DecimalField(max_digits=5,decimal_places=2);
    year=models.PositiveIntegerField();
    
    def __str__(self):
        return "Obtained %d in %s at %s in year %d" % (self.marks,self.course,self.uni,self.year)

class personal(models.Model):
     primary_table=models.ForeignKey('student', null=False);
     mother_name=models.CharField(max_length=20);
     father_name=models.CharField(max_length=20);
     mother_occupation=models.CharField(max_length=20);

     father_occupation=models.CharField(max_length=20);
     languages=models.CharField(max_length=100);
     hobbies=models.CharField(max_length=100);
     per_address=models.CharField(max_length=200);
     corr_address=models.CharField(max_length=200);
     def __str__(self):
        return "Personal details about %s (%s)" % (self.primary_table.fullname, self.primary_table.prn);

class software_exposure(models.Model):
    primary_table=models.ForeignKey('student', null=False);
    programming_languages = models.CharField(max_length=100);
    databases = models.CharField(max_length=100)
    OS = models.CharField(max_length=100)
    sw_packages = models.CharField(max_length=100)
    web_tools = models.CharField(max_length=100)
    def __str__(self):
        return "Software Exposure of %s(%s)" % (self.primary_table.fullname, self.primary_table.prn);

class ExtraField(models.Model):
    primary_table=models.ForeignKey('student');
    title=models.CharField(blank=False,max_length=20);
    description = models.CharField(blank=False,max_length=100);
    from_date = models.DateField();
    end_date = models.DateField(null=True,blank=True);
    def __str__(self):
        return "Details about %s of %s" % (self.title,self.primary_table.fullname);

class workex(ExtraField):
    #title=models.CharField(default="workex", editable=False); -- think of a way to override the titile so that the title is always Eorkex.. or do we do that while taking the input???
    pass;
        
class certification(ExtraField):
    pass;

class projects(ExtraField):
    pass;

class academic_acheivement(ExtraField):
    pass;

class extra_curricular(ExtraField):
    pass;

"""
#In sabko ume actually use karna hai jab hum version treat karenge au

class ExtraTable(models.Model):
    tables = (('p','personal'),('sw','software_exposure'),('ex','extraField'),('m','marks'),('s','student'))
    Column_Type = (('MVOLD','Multi-valued one line display'),
                   ('MVMLD','Multi-valued multiple line display'),
                   ('SVOLD','Single-valued one line display')
                   );

    column_name = Models.CharField(max_length=50);
    column_type = Models.CharField(max_length=5,choices=Column_Type);
    column_length = Models.PositiveIntegerField();
    column_title = Models.CharField(max_length=2,choices=tables);

class ExtraTableKaData(models.Model):
    field = models.ForeignKey('ExtraTable');
    data = models.TextField();
"""
