from company.models import *
from django.contrib import admin
#from djamgo.core.mail import send_  mail

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
'''    inlines = [
        membershipInline,
        ]

#    def informStudents(self, request, selected_companies):
#        for c in selected_companies:
#            for g in c.came_for_group.values():
#                students = objects.selected
'''
admin.site.register(company,companyAdmin);

admin.site.register(placement_in);

