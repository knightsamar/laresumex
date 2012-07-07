from django.forms import ModelForm
from student_info.models import personal, marks, swExposure, certification, workex, academic, project, extracurricular, student
from django.forms.extras.widgets import SelectDateWidget

def getYears(**kwargs):
    from datetime import datetime;
    presentYear = datetime.now().year
    years = []
    if 'previousYears' in kwargs and 'nextYears' in kwargs:
        start = presentYear - 30
        end = presentYear + 3
    elif 'previousYears' in kwargs and not 'nextYears' in kwargs:
       #TODO: We need to have a CORRECT limit year on the right side
        start = presentYear - 30
        end = presentYear

    for y in range(start,end):
        years.append(y)

    return years

class PersonalForm(ModelForm):
    class Meta:
        model = personal;
        exclude=('primary_table','prn','backlogs','yeardrop','certification','project','academic','extracurricular','workex','Extra_field','last_update')
        widgets = {
                'birthdate' : SelectDateWidget(years = getYears(previousYears=30))
               }

class MarksForm(ModelForm):
    class Meta:
        model = marks;
        exclude = ('id','primary_table')
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }
        
class SwExposureForm(ModelForm):
    class Meta:
        model = swExposure
        exclude=('primary_table')

class CertificationForm(ModelForm):
    class Meta:
        model = certification

        #define the order of the fields on the form
        fields = ('title','desc','fromDate','endDate')

        exclude=('primary_table')
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3)),
                'endDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }

class WorkexForm(ModelForm):
    class Meta:
        model = workex
        exclude = ('primary_table')

        #define the order of the fields on the form
        fields = ('title','desc','fromDate','endDate')

        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3)),
                'endDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }

class AcademicAchievementsForm(ModelForm):
    class Meta:
        model = academic
        exclude = ('primary_table')

        #define the order of the fields on the form
        fields = ('title','desc','fromDate','endDate')
 
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3)),
                'endDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }

class ProjectForm(ModelForm):
    class Meta:
        model = project
        exclude = ('primary_table')

        #define the order of the fields on the form
        fields = ('heading','title','desc','fromDate','endDate')
                
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3)),
                'endDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }

class ExtraCurricularForm(ModelForm):
    class Meta:
        model = extracurricular
        exclude = ('primary_table')

        #define the order of the fields on the form
        fields = ('title','desc','fromDate','endDate')
 
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3)),
                'endDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }

class StudentForm(ModelForm):
    class Meta:
        model = student
        exclude = ('prn','backlogs','yeardrops','certification','project','academic','extracurricular','workex','Extra_field','last_update')
        
        #define the order of the fields on the form
        fields = ('fullname','sex','email','phone','career_objective')
