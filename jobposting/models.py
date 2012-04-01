from django.db import models
from ldap_login.models import user, group
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from student_info.models import student
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q


class personalised_posting(models.Model):
    post= models.ForeignKey('posting');
    is_interested = models.BooleanField();
    is_hidden = models.BooleanField();
    prn = models.ForeignKey('ldap_login.user')
    def __str__(self):
        return "job posting of %s for %s" % (self.prn.username , self.post.company_name)
 
class posting(models.Model):
    '''described the Job Posting model.
       WARNING: any changes made to this need to be reflected in the corresponding ModelForm in forms.py too!
    '''
    eligible_groups = Q(name__icontains = '142') | Q(name__icontains = '141') | Q(name__icontains = '121') | Q(name__icontains = '122') | Q(name__icontains = 'laresumex')

    company_name=models.CharField(max_length=50,blank=False,verbose_name='Organization\'s Name');
    company_url=models.URLField(verify_exists=True,verbose_name='Website address');
    description=models.TextField(blank=False,verbose_name='Description',help_text='Please tell in details about the job profile, eligibility, etc');
    how_to_apply=models.TextField(blank=False,help_text='Please tell how students can apply');
    posted_by=models.CharField(max_length=30,blank=False)
    non_sicsr_poster=models.BooleanField(verbose_name='Posted by SICSR user?', default=False,blank=False,null=False) #to determine whether to use ldap_login or other auth sources
    posted_on=models.DateTimeField(auto_now_add=True,editable=False);
    #tally  = models.IntegerField(default=0, verbose_name = "No of Students that have shown interest in this company", editable = False);
    approved_on = models.DateTimeField(editable = False,null = True , blank =True);
    post_status=(('p','pending'),('a','approved'),('d','disapproved'));
    status=models.CharField(verbose_name='Job Posting status',max_length=1,choices=post_status, default = 'p');

    for_programmes = models.ManyToManyField(group,verbose_name="Eligible Groups",limit_choices_to=eligible_groups)

    def test(self):
        self.company_name = "ha ha ha ";
        self.save();
        return "hooooohooooo"

    def __str__(self):
        return "job posting about %s by %s " % (self.company_name, self.posted_by);

    def tally(self):
        #count = personalised_posting.objects.filter(post = self).aggregate(count = 'is_interested = True')
        count = personalised_posting.objects.filter(post=self).filter(is_interested=True).count();
        return count;

def handle_new_posting(sender, **kwargs):
    '''Signal handler whenever a job posting is created
       Refer: http://localhost/docs/django-docs/ref/signals.html#django.db.models.signals.post_save
    '''

    if sender == posting:
        if kwargs['created'] == False: #we want to handle only APPROVED jobpostings (right ?)
            jp = kwargs['instance']
            print dir(jp)
            print jp.get_status_display()
            if jp.get_status_display() != 'approved': #ONLY do the things on APPROVED job postings
                print "Not approved, returning"
                return
            
            print "Processing, it's approved"
            
            to_be_emailed = []; #list of email addresses to be emailed
            print "For jobposting ", jp
            for g in jp.for_streams.all():
                print 'Got group',g
                for u in g.user_set.all():
                    print 'Got user',u
                    try:
                        to_be_emailed.append("%s@sicsr.ac.in" % (u.username))
                        to_be_emailed.append(student.objects.get(prn=u.username)).email
                    except ObjectDoesNotExist:
                        print "%s hasn't yet filled in details...so couldn't get his personal email address" % u.username
                    except Exception as e:
                        print e
            full_name = u.fullname if u.fullname.strip()!= '' else u.username

            html_content = """
             Hi,

             A new job posting has been put up on LaResume-X by <b>%s</b>.

             To view it go <a href='http://projects.sdrclabs.in/laresumex/jobposting/views/view'>here</a>
             
             Thanks!

             Regards,
             Team LaResume-X
            """ % (full_name)

            text_content = """
             Hi,

             A new job posting has been put up on LaResume-X by %s.

             To view it go to http://projects.sdrclabs.in/laresumex/jobposting/views/view
             
             Thanks!

             Regards,
             Team LaResume-X
             """ % (full_name) 
            email = EmailMultiAlternatives('[LaResume-X]New job posting',text_content)
            email.attach_alternative(html_content, 'text/html')
            email.bcc = '10030142031@sicsr.ac.in'
            email.bcc = '10030142056@sicsr.ac.in'
            email.bcc = to_be_emailed;

            email.subject = "[LaResume-X] New job posting"
            email.send()
            
#Whenever a posting is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
post_save.connect(handle_new_posting,sender=posting,weak=False,dispatch_uid='hamaraSignalwa');   
