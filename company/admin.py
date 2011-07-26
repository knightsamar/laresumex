from company.models import *
from django.contrib import admin
class companyAdmin(admin.ModelAdmin):
    __name__='CompanyAdmin';
    readonly_fields = ['students_applied']; #will display this field as a link rather than editable box
    
    #for list display
    list_display = ('name','date_of_process','last_date_of_applying')
    list_filter = ['came_for_group'];

admin.site.register(company,companyAdmin);


