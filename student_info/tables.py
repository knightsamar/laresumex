from student_info.models import *
from laresumex.settings import MEDIA_URL,ROOT
from student_info.utility import our_redirect 

def get_tables(s):

        tables = {'p':'personal', 'c':'certification','sw':'swExposure','m':'marks','pro':'project','a':'academic','w':'workex', 'e':'extracurricular'}
        included=['strongAreas','weakAreas']
        
        
        #removing the workex... from the extra fields to get the unnamed extra fields ;) Not a very good idea. need to think of a way to first get all extra fields and then seggregate them into different things.fields
        maintable=list(companySpecific.objects.all());
        cs=list(companySpecificData.objects.filter(primary_table=s))
        k=0
        csd=dict()
        for css in range(len(cs)):
            if cs[k].valueOf in maintable:
                i=maintable.index(cs[k].valueOf)
                maintable.remove(maintable[i])
            if str(cs[k].valueOf.key) in included:
                csd[cs[k].valueOf.key]=cs[k];
                cs.remove(cs[k])
                k = k-1
            k = k+1;   
        print "CS ====",cs
        print "CSD====",csd
        print "Maintable....",maintable
        ex=list(ExtraField.objects.filter(primary_table=s));
        print ex
        k=0
        for ee in range(len(ex)):
                print k
                print "got", ex[k].title 
                if str(ex[k].title) in tables.values():
                    ex.remove(ex[k])
                    
                    k = k-1
                k = k+1
                print 'k ===',k
                print 'ee==',ee
                print ex       
        #ex=ExtraField.objects.exclude(title__in=tables.values())

        for t,v in tables.iteritems():
            print "=========>>", v  ,"<<======="
            if (t is not 'p') and (t is not 'sw'):
                tables[t]=eval(v).objects.filter(primary_table=s).order_by('fromDate');
            else:
                try:
                  tables[t]=eval(v).objects.get(primary_table=s)
                except Exception as e:
                    pass;
        tables['s']=s;   
        tables['ex']=ex
        tables['ROOT']=ROOT
        tables['cs']=cs
        tables['csd']=csd
        tables['mt']=maintable
        tables['MEDIA_URL']=MEDIA_URL
        return tables
