from django.db import models

# Create your models here.

class company(models.Model):
    name=models.CharField(max_length=40);
    last_date_of_applying=models.DateField();
    students_applied=models.ManyToManyField('student_info.student')
    date_of_process=models.DateField();
    email_id=models.EmailField();
    phone_number=models.CharField(max_length=15)
    #comapny_url=models.CharField(max_length=20)
    #came_for_group=models.ManyToManyField('ldap_login/group')
    eligibilty=models.TextField();
    

    def __str__(self):
        return "%s came/will come on %s" % (self.name,self.date_of_process);
