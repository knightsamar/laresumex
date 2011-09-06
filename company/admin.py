from company.models import *
from django.contrib import admin
from student_info.models import student; #for mailing the student on his personal mail address.
from django.core.mail import send_mass_mail
#from django.template import Context, loader, Request

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

    def informStudents(self, request, selectedCompanies):
        print "Informing students about ",selectedCompanies;

        t = loader.get_template('company/informStudents_mail.html');
        for c in selectedCompanies:
            ppltoInform = c.came_for_group.get_query_set()[0].user_set.all() 
            context = Context(
                    {'c' : c }
                    )
            mail_body = t.render(c);
            to = [];
            for p in ppltoInform:
                s = student.objects.get(prn=p.username);
                to.append(s.email); #add secondary address
                #whether to use it or not is the call of Placement Team
                to.append("%s@sicsr.ac.in" % p.username); #for primary sicsrwala address
            send_mass_mail("[Placements] %s coming on campus" % c.name,mail_body,"placements@sicsr.ac.in",to,fail_silently=True);

admin.site.register(company,companyAdmin);
admin.site.register(placement_in);

