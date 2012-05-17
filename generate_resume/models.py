from django.db import models
from student_info.models import student;
from laresumex.settings import RESUME_STORE
from os import path
# Create your models here.
class resume(models.Model):
    prn = models.ForeignKey('student_info.student',help_text="PRN of the student who's resume was generated",unique=True);
    last_tex_generated = models.DateTimeField(help_text="When was this student's .tex file last generated ?",null=True);
    last_pdf_generated = models.DateTimeField(help_text="When was this student's .pdf file last generated ?",null=True);
    
    def __str__(self):
        return "resume record of %s " % (self.prn);

    def get_pdf_path(self):
        '''will get the path to the PDF copy of the resume'''
        if self.last_pdf_generated is not None:
            pdf_path = '%s/resumes/%s.pdf' % (RESUME_STORE, self.prn.prn)
            #does this PDF actually exist ?
            if path.exists(pdf_path):
                return pdf_path
            else:
                print '%s does not exist, needs to be generated!' % pdf_path
                pisapdf(None,self.prn,False)
        return None
