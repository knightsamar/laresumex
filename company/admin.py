from company.models import *
from django.contrib import admin
from student_info.models import student; #for mailing the student on his personal mail address.
from django.core.mail import EmailMessage,get_connection #because this one actually let's use BCC and all.
from django.template import Context, loader
from laresumex.settings import MANAGERS;
from django.http import HttpResponse
from datetime import datetime
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
    actions = ['informStudents','list_interested_students'];

    def informStudents(self, request, selectedCompanies):
        print "Informing students about ",selectedCompanies;

        t = loader.get_template('company/informStudents_mail.html');
        conn = get_connection(); #for mailing
        
        for c in selectedCompanies:
            #don't send email intimations about old company arrivals wrongly as done on Sat Mar 17.

            if c.date_of_process < datetime.today(): #company process date has already passed
               print "Not informing because date of process %s has already passed!!" % (c.date_of_process)
               continue
                
            ppltoInform = c.came_for_group.get_query_set()[0].user_set.all() 
            context = Context(
                {
                    'company' : c,
                })

            body = t.render(context)

            to = [];
            for p in ppltoInform:
                to += ["%s@sicsr.ac.in" % str(p.username)]; #for primary sicsrwala address
       
            #send mail actually.
            email = EmailMessage();
            email.from_email = '"Ashwini Narayan" <placements@sicsr.ac.in>';
            email.subject = '[Placements] %s coming to campus' % c.name;
            #email.from = 'root@sdrcserver.sdrc'; #left for automatic putting
            email.connection = conn;
            email.body = body;
            
            cc = [];
            # Getting the From/ CC from the placement Committee group.
            from django.contrib.auth.models import Group;
            g = Group.objects.get(name = 'placement committee')
            
            for u in g.user_set.all():
               cc.append(u.email)
            
            bcc = []
            for m in MANAGERS:
                bcc.append(list(m)[1])
            
            email.to = to + cc;
            email.bcc = bcc;
            print "to is ",email.to;
            print "bcc is ",email.bcc;
            print "body is ",email.body
            email.content_subtype='html';
            email.send();
            dir(email)
            print "Done with %s" % (c);

        self.message_user(request,"Successfully informd students");    
    informStudents.short_description = "Inform students about companies"

    def list_interested_students(self , request , selectedCompanies):
		print "Listing students who are interested ",selectedCompanies;
		StudentDict = {}
		#saglaya selectedCompanies tun
		
		for company in selectedCompanies:
			#pratyek company saathi
			interested_students = company.get_interested_students()
			#jya students ne apply kela tyancha obejct store kara
			if len(interested_students) == 1:
		            	StudentDict['%s : %d student' % (str(company.name),len(interested_students))] = interested_students;
			if len(interested_students) != 1:
			     StudentDict['%s : %d students' % (str(company.name),len(interested_students))] = interested_students;

		print StudentDict;
		t = loader.get_template("company/interested_students_list.html");
		c = Context ({ 'appliedStudents' : StudentDict });
		return HttpResponse(t.render(c));
    list_interested_students.short_description="List interested students !";

class placement_inAdmin(admin.ModelAdmin):
    list_filter = ['company']

admin.site.register(company,companyAdmin);
admin.site.register(placement_in,placement_inAdmin);

