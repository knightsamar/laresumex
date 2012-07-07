from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

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

    #contact
    #(r'^/$',"generate_resume.views.index"),   
    (r'^common/(?P<msg>\D+)/done',"common.views.done"),
    (r'^contact',"common.views.contact"),
    
    #jobposting
    (r'^jobposting/add$',"jobposting.views.add"),
    (r'^jobposting/view_hidden$',"jobposting.views.hidden"),
    (r'^jobposting/(?P<template>\D+)/view$',"jobposting.views.view"),
    (r'^jobposting/(?P<template>\D+)/do$',"jobposting.views.do"),
    (r'^jobposting/(?P<jp>\d+)/get_interested_students$',"jobposting.views.get_interested_students"),

    # generate_resume
    (r'^generate_resume/(?P<prn>\d+)/pdf',"generate_resume.views.pdf"),
    (r'^generate_resume/(?P<prn>\d+)/html',"generate_resume.views.html"),
    (r'^generate_resume/(?P<prn>\d+)/pisapdf',"generate_resume.views.pisapdf"), #the non-latex pisa and reportlab based pdf generator

    #(r'^generate_resume/(?P<prn>\d+)/latex',"generate_resume.views.latex"),
    
    #ldap_login
    (r'^ldap_login/$','ldap_login.views.login'), #for authentication
    (r'^ldap_login/logout$','ldap_login.views.logout'), #for loggin out
    (r'^ldap_login/passwordHelp$','ldap_login.views.passwordHelp'),
    (r'^home/$',"common.views.index"),
    (r'^$','common.views.index'),
    
    # company
    (r'^company/getResume',"company.views.getResume"),
    (r'^company/list',"company.views.company_list"),
    (r'^company/get_student_name',"company.views.get_students_name"),
    (r'^company/apply',"company.views.apply"),
    (r'^company/search',"company.views.search"),
    (r'^PT/admin',"company.views.admin_index"),
    (r'^PT/fetch',"company.views.fetch_index"),
    (r'^PT/reports',"company.views.got_placed"),
    
    # student_info
    (r'^student_info/(?P<prn>\d+)/form',"student_info.views.nayeforms"),
    (r'^student_info/(?P<prn>\d+)/nayaform',"student_info.views.nayeforms"),

    #trying out django social auth
    (r'^socialauth/login/',"socialauth.views.loginHandler"),
    (r'^socialauth/loggedin/',"socialauth.views.logged_in"),
    (r'^socialauth/logout/',"socialauth.views.logout"), 
    url(r'',include('social_auth.urls')),

    #for ldap login 
    (r'^login/$','common.views.login'),
    (r'^logout/$','common.views.logout'),

    (r'^foo/$','student_info.views.foo'),
)
