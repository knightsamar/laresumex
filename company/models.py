from django.db import models
from student_info.models import student

# Create your models here.

class company(models.Model):
    name=models.CharField(max_length=40);
    last_date_of_applying=models.DateTimeField();
    students_applied=models.ManyToManyField('student_info.student',blank=True)
    date_of_process=models.DateTimeField();
    email_id=models.EmailField(help_text='Email of the Company contact (will not be displayed to students)');
    phone_number=models.CharField(max_length=20,help_text='Phone number of the Company contact (will not be displayed to students)')
    #comapny_url=models.CharField(max_length=20)
    came_for_group=models.ManyToManyField('ldap_login.group',help_text='Eligible group of students')
    eligibilty=models.TextField(help_text='Elgibility and other such information to be displayed to students');

    def __str__(self):
        return "%s" % (self.name);

    class Meta:
         verbose_name_plural = "companies"

class placement_in(models.Model):
    jobtype=(('i',"Internship"),('p',"placement"),('pi','placement + internship'))
    
    student= models.ForeignKey('student_info.student');
    comapny = models.ForeignKey('company');
    profile = models.CharField(max_length=50);
    placementType = models.NullBooleanField(choices=jobtype)
    date_of_joining = models.DateField();
    starting_stipen = models.DecimalField(max_digits = 5 , decimal_places =2, null=True , blank = True);
    offered_salary = models.DecimalField(max_digits = 5 , decimal_places =2, null=True , blank = True);
    place = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return "%s got %s in %s " %(self.primary_table.prn, self.placementType, self.comapny.name)

    class Meta:
        verbose_name_plural = 'Which Student Got Placements';


