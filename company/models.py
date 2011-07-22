from django.db import models

# Create your models here.

class company(models.Model):
    name=models.CharField(max_length=40);
    date_of_interview=models.DateField();
    students_applied=models.ManyToManyField('student_info.student')
    def __str__(self):
        return "%s came/will come on %s" % (self.name,self.date_of_interview);
