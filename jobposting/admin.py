from jobposting.models import *
from django.contrib import admin

class personalizedPostingAdmin(admin.ModelAdmin):
    list_filter = ['post','is_interested'];

def approve(modeladmin, request, queryset):
    queryset.update(status='d');
approve.short_description="Approve selected";

class postingAdmin(admin.ModelAdmin):
    list_display= ['__str__','status', 'tally'];
    list_filter = ['status']
    search_fields = ['company_name']
    def approve(self, request, queryset):
        r = queryset.update(status='a');
        if r == 1:
            message_bit = "1 posting was approved"
        else:
            message_bit = "%s postings are now approved" %r;
        self.message_user(request,message_bit);    
    approve.short_description="Approve selected";

    actions = [approve];

    
admin.site.register(posting,postingAdmin);
admin.site.register(personalised_posting,personalizedPostingAdmin);

