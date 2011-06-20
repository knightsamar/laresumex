from django.db import models

# Create your models here.

class student(models.Model):
    prn = models.CharField(max_length=12);
    fullname = models.CharField("Full Name", max_length=60, help_text="FULL NAME As on your certificates", blank=False,null=False);
    father_name = models.CharField("Father's Name", max_length=30,blank=True);
    mother_name = models.CharField("Mother's Name", max_length=30,blank=True);

    def __str__(self):
        return "%s(%s)" % (self.fullname, self.prn);

