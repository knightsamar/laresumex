from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^laresumex/', include('laresumex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),

    # actually our urls START FROM NOW
    

    # generate_Resume
    (r'generate_resume/(?P<prn>\d+)/latex_sample',"generate_resume.views.latex_sample"),
    (r'generate_resume/(?P<prn>\d+)/pdf',"generate_resume.views.pdf"),
    (r'generate_resume/(?P<prn>\d+)/html',"generate_resume.views.html"),
    (r'generate_resume/(?P<prn>\d+)/latex',"generate_resume.views.latex"),
    
    #ldap_login
    (r'^ldap_login/$','ldap_login.views.login'), #for authentication
    (r'^ldap_login/logout$','ldap_login.views.logout'), #for loggin out
    (r'home',"generate_resume.views.index"),
    
    # company
    (r'search',"company.views.search"),
    (r'company/getResume',"company.views.getResume"),
    
    # sudent_info
    (r'student_info/(?P<prn>\d+)/edit',"student_info.views.edit"),
    (r'student_info/form',"student_info.views.showform"),
    (r'student_info/(?P<prn>\d+)/submit',"student_info.views.submit"),
    (r'form',"student_info.views.showform"),
)
