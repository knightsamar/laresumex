from django.db import models
# Create your models here.

#one group has many users
class group(models.Model):
    name = models.CharField(max_length=20,unique=True);
    created_on = models.DateTimeField(auto_now_add=True);

    def __str__(self):
            Three_yr_courses={ 122:'BBA(IT)',121:'BCA'}
            Two_yr_courses={ 142:'MSc(CA)',141:'MBA(IT)'}
            if self.name[5:8] in Three_yr_courses.keys():
                a=3
                curse=Three_yr_courses[self.name[:2]]
            else:
                a=2
                curse=Two_yr_courses[int(self.name[5:8])]
            yr=curse+" "+str(self.name[:2]) + '-' + str(a+int(self.name[:2])) 
            return yr;

#many user belongs to one group
class user(models.Model): 
    username = models.CharField(max_length=30,primary_key=True); #without the domain suffix
    #password = models.CharField(max_length=255,blank=True,null=True); #we may or many not store the password;
    #last_login = models.DateTimeField(auto_now=True);
    created_on = models.DateTimeField(auto_now_add=True);
    groups = models.ManyToManyField(group);


    def __str__(self):
	    return self.username;


