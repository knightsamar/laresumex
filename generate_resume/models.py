from django.db import models
from student_info.models import student;

# Create your models here.
class resume(models.Model):
    prn = models.ForeignKey('student_info.student',help_text="PRN of the student who's resume was generated");
    last_tex_generated = models.DateTimeField(auto_now=True,help_text="When was this student's .tex file last generated ?");
    last_pdf_generated = models.DateTimeField(auto_now=True,help_text="Ok...i don't know why this is here!");

    def __str__(self):
        return "resume record of %s " % (self.prn);


