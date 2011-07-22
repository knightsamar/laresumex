from django.db import models
# Create your models here.

#many user belongs to one group
class user(models.Model): 
    username = models.CharField(max_length=30,primary_key=True); #without the domain suffix
    last_login = models.DateTimeField(auto_now=True);
    created_on = models.DateTimeField(auto_now_add=True);

    def __str__(self):
	return self.username;


