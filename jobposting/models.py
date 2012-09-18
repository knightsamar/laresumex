from django.db import models
from ldap_login.models import user, group
from django.db.models.signals import post_save
from student_info.models import student
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.db.models import Q
from smtplib import SMTPException 
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from laresumex.settings import MANAGERS
from generate_resume.models import resume
from ldap_login.models import user

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
    post_status=(('p','pending approval'),('a','approved'),('d','disapproved'));

    company_name=models.CharField(max_length=50,blank=False,verbose_name='Organization\'s Name');
    company_url=models.URLField(verify_exists=True,verbose_name='Website address');
    description=models.TextField(blank=False,verbose_name='Description',help_text='Please tell in details about the job profile, eligibility, etc');
    how_to_apply=models.TextField(blank=False,help_text='Please tell how students can apply');
    posted_by=models.CharField(max_length=30,blank=False)
    non_sicsr_poster=models.BooleanField(verbose_name='Posted by Non-SICSR user?', default=False,blank=False,null=False) #to determine whether to use ldap_login or other auth sources
    posted_on=models.DateTimeField(auto_now_add=True);
    #tally  = models.IntegerField(default=0, verbose_name = "No of Students that have shown interest in this company", editable = False);
    approved_on = models.DateTimeField(null = True , blank =True, editable = False);
    status=models.CharField(verbose_name='Job Posting status',max_length=1,choices=post_status, default = 'p');

    for_programmes = models.ManyToManyField(group,verbose_name="Eligible Batches",limit_choices_to=eligible_groups,help_text='These batches will be informed by email about this Job posting.')

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
    
    def get_interested_students(self):
        '''Returns a data structure of interested students for this job posting
           This data structure is a dictionary of dictionaries which contain various informations about the interested student
        '''
        pps = personalised_posting.objects.filter(post=self).filter(is_interested=True)
        interested_students = {}

        for p in pps:
            interested_students[str(p.prn)] = {
                    'has_resume': resume.can_resume_be_generated(p.prn),
                    'name' : user.objects.get(username=p.prn).fullname,
                    }

        print "List of interested students is ", interested_students
        return interested_students

def handle_new_posting(sender, **kwargs):
    '''Signal handler whenever a job posting is created
       Refer: http://localhost/docs/django-docs/ref/signals.html#django.db.models.signals.post_save
    
       This signal handler does the following:
       
       If a jobposting is approved:
            Emails all the eligible group students the jobposting.

    '''

    if sender == posting:
        if kwargs['created'] == False: #we want to handle only APPROVED jobpostings 
            jp = kwargs['instance']
            print dir(jp)
            print jp.get_status_display()
            if jp.get_status_display() != 'approved': #ONLY do the things on APPROVED job postings
                print "Not approved, returning"
                return
            
            print "Processing, it's approved"
            try:
                to_be_emailed = []; #list of email addresses to be emailed
                print "For jobposting ", jp
                for g in jp.for_programmes.all():
                    print 'Got group',g
                    for u in g.user_set.all():
                        print 'Got user',u.username
                        try:
                            to_be_emailed.append("%s@sicsr.ac.in" % (u.username))
                            c = student.objects.get(prn=u.username)
                            if c is student:
                               to_be_emailed.append(student.objects.get(prn=u.username)).email

                        except student.DoesNotExist as s:
                            print "%s hasn't yet filled in details...so couldn't get his personal email address" % u.username
                            continue;
                        except Exception as e:
                            print e
                            continue;

                poster_id = jp.posted_by
                poster_full_name = "Unknown User"

                if jp.non_sicsr_poster:
                    record = User.objects.get(username=poster_id)
                    poster_full_name = record.get_full_name() if record.get_full_name().strip()!= '' else record.username
                    #TODO: to get the provider name properly and fix this
                    #provider = UserSocialAuth.objects.get(uid=poster_id).provider
                    #poster_full_name = "%s from %s" % (poster_full_name, provider)
                else:
                    u = user.objects.get(username = poster_id)
                    poster_full_name = u.fullname if u.fullname.strip()!= '' else u.username
                
                print "Poster's Full name : ", poster_full_name

                html_content = """
                 Hi,

                 A new job posting has been put up on LaResume-X by <b>%s</b> for <b>%s</b>.

                 It's detail are as follows :
                 <ul>
                    <li>Organization's Website: %s </li> 
                    <li>Description:
                    <p>%s</p>
                    </li>
                    <li>How to Apply ? %s </li>
                 </ul>
                 To register your interest in it go to <a href='http://projects.sdrclabs.in/laresumex/jobposting/views/view'>here</a>
                 
                 <br/>
                 Thanks!
                 <br/>
                 Regards,<br/>
                 Team LaResume-X
                """ % (poster_full_name, jp.company_name, jp.company_url, jp.description, jp.how_to_apply)

                text_content = """
                 Hi,

                 A new job posting has been put up on LaResume-X by %s for %s.

                 To register your interest in it go to http://projects.sdrclabs.in/laresumex/jobposting/views/view

                 It's detail are as follows :
                 Organization's Website: %s  
                 Description: %s 
                 How to Apply ? %s 
                 
                 
                 Thanks!

                 Regards,
                 Team LaResume-X
                 """  % (poster_full_name, jp.company_name, jp.company_url, jp.description, jp.how_to_apply)
                email = EmailMultiAlternatives('[LaResume-X]New job posting',text_content)
                email.attach_alternative(html_content, 'text/html')
                
                #add the managers 
                for x in MANAGERS:
                    email.bcc.append(x[1]);

                email.bcc = to_be_emailed;

                email.subject = "[LaResume-X] New job posting"
                email.send(fail_silently=False)
                print "Sent email succesfully to ", to_be_emailed
                print "Total addresses emailed  :", len(to_be_emailed) 
            except SMTPException as e:
                print 'Exception occured when trying to actually send the email'
                print e
            except Exception as e:
                print 'Exception occurred when constructing email messages'
                print e
                mail_managers(subject = "Emailing problem",
                message = "Couldn't send email about jobposting for %s by %s" % (jp.company_name, poster_full_name),
                fail_silently = False)


#Whenever a posting is saved, signal!
#Refer: http://localhost/docs/django-docs/topics/signals.html#listening-to-signals for syntax of the below and why weak is kept False.
post_save.connect(handle_new_posting,sender=posting,weak=False,dispatch_uid='hamaraSignalwa');   

