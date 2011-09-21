from django.db import models

# Create your models here.

class posting(models.Model):
    '''described the Job Posting model.
       WARNING: any changes made to this need to be reflected in the corresponding ModelForm in forms.py too!
    '''
    company_name=models.CharField(max_length=50,blank=False,verbose_name='Organization\'s Name');
    company_url=models.URLField(verify_exists=True,verbose_name='Website address');
    description=models.TextField(blank=False,verbose_name='Description',help_text='Please tell in details about the job profile, eligibility, etc');
    how_to_apply=models.TextField(blank=False,help_text='Please tell how students can apply');
    posted_by=models.CharField(max_length=12,blank=False);
    posted_on=models.DateTimeField(auto_now_add=True,editable=False);

    def __str__(self):
        return "posting for %s by %s " % (self.company_name, self.posted_by);
