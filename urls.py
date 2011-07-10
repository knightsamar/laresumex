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
    (r'generate_resume/(?P<prn>\d+)/latex',"generate_resume.views.latex"),
    (r'home',"generate_resume.views.index"),
    (r'generate_resume/(?P<prn>\d+)/pdf',"generate_resume.views.pdf"),
    (r'student_info/(?P<prn>\d+)/edit',"student_info.views.edit"),
    (r'student_info/form',"student_info.views.showform"),
    (r'student_info/(?P<prn>\d+)/submit',"student_info.views.submit"),
    (r'form',"student_info.views.showform"),
    (r'generate_resume/(?P<prn>\d+)/html',"generate_resume.views.html"),
)
