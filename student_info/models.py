from django.db import models

# Create your models here.

class student(models.Model):
    gender=(('m',"Male"),('f',"female"))
    
    prn = models.CharField(max_length=12,unique=True,primary_key=True);
    fullname = models.CharField("Full Name", max_length=60, help_text="FULL NAME As on your certificates", blank=False,null=False)
    sex=models.CharField(max_length=1,choices=gender);
    age=models.PositiveSmallIntegerField();
    email=models.EmailField(max_length=75);
    phone_number=models.PositiveIntegerField(max_length=10);
    career_objective=models.TextField(blank=False);
    #marks = models.ForeignKey('marks',null=True);
    #software_exposure=models.BooleanField(null=False);
    #workex=models.ForeignKey('workex',null=True);

    certification=models.BooleanField();
    Projects=models.BooleanField();
    acedemic_qualifications=models.BooleanField();
    Extra_curricular=models.BooleanField();
   # Extra_field=models.NullBooleanField(null=True);
   
    def __str__(self):
        return " Resume details of %s(%s)" % (self.fullname, self.prn);
 
class marks(models.Model):
    primary_table=models.ForeignKey('student');
    course=models.CharField(max_length=10, null=False);
    uni=models.CharField(max_length=20);
    marks=models.DecimalField(max_digits=5,decimal_places=2);
    year=models.PositiveIntegerField();
    
    def __str__(self):
        return "Obtained %d in %s at %s in year %d" % (self.marks,self.course,self.uni,self.year)
class personal(models.Model):
    primary_table=models.ForeignKey('student');
    

 
class ExtraField(models.Model):
    primary_table=models.ForeignKey('student');
    title=models.CharField(blank=False,max_length=20);
    description = models.CharField(blank=False,max_length=100);
    from_date = models.DateField();
    end_date = models.DateField(null=True);
    def __str__(self):
        return "Details about %s of %s" % (self.title,self.primary_table.fullname);

class workex(ExtraField):
    #title=models.CharField(default="workex", editable=False); -- think of a way to override the titile so that the title is always Eorkex.. or do we do that while taking the input???
    pass;
class certification(ExtraField):
  pass;
class projects(ExtraField):
   pass;
class acedemic_acheivement(ExtraField):
    pass;
class extra_curricular(ExtraField):
    pass;

    

