from django.db import models
from ldap_login import user;

# Create your models here.

class posting(models.Model):
    company_name=models.CharField(max_length=50);
    company_url=models.CharField(max_length=50);
    how_to_apply=models.TextField();
    profile=models.TextField();
    posted_by=models.ForeignKey('ldap_login/user');
    posted_on=models.DateTimeFields(auto_add_now=True);

    def __str__(self):
        return "posting for %s %self.company_name";
