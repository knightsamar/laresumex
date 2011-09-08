from company.models import *
from django.contrib import admin
from student_info.models import student; #for mailing the student on his personal mail address.
from django.core.mail import EmailMessage,get_connection #because this one actually let's use BCC and all.
from django.template import Context, loader

'''
class membershipInline(admin.TabularInline):
    model = student_info.placement_in.set; #a reference to the intermediary modeli
    extra = 1
#    fk_name = 'placement_in'
'''

class companyAdmin(admin.ModelAdmin):
    __name__='CompanyAdmin';
    readonly_fields = ['students_applied']; #will display this field as a link rather than editable box
    
    #for list display
    list_display = ('name','date_of_process','last_date_of_applying')
    list_filter = ['came_for_group'];
    #inlines = [
    #    membershipInline,
    #    ]
    
    #add a set of actions
    actions = ['informStudents'];

    def informStudents(self, request, selectedCompanies):
        print "Informing students about ",selectedCompanies;

        t = loader.get_template('company/informStudents_mail.html');
        conn = get_connection(); #for mailing
        for c in selectedCompanies:
            ppltoInform = c.came_for_group.get_query_set()[0].user_set.all() 

            for p in ppltoInform:
                s = student.objects.get(prn=p.username);
                to = [s.email]; #add secondary address
                to += ["%s@sicsr.ac.in" % p.username]; #for primary sicsrwala address
        
                context = Context(
                {
                    'company' : c,
                    'student' : s, #khamakha templating engine usage, and ultimately more processing time.
                })

                body = t.render(context)

                #send mail actually.
                email = EmailMessage();
                email.from_email = 'knightsamar@ssiknight';
                email.subject = '[Placements] %s coming to campus' % c.name;
                #email.from = 'root@sdrcserver.sdrc'; #left for automatic putting
                email.connection = conn;
                email.body = body;
                email.bcc = to; #so as to maintain privacy.
                email.to = ['samar@sicsr.ac.in'];
                email.content_subtype='html';
                email.send();
                dir(email)
                print email.bcc;
                print body; 
                print "Done with %s" % (c);

    informStudents.short_description = "Inform students about companies"

admin.site.register(company,companyAdmin);
admin.site.register(placement_in);

