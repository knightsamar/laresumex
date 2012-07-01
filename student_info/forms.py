from django.forms import ModelForm
from student_info.models import personal, marks
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

class MarksForm(ModelForm):
    class Meta:
        model = marks;
        exclude = ('id','primary_table')
        widgets = {
                'fromDate' : SelectDateWidget(years = getYears(previousYears=30,nextYears=3))
                }
        
class PersonalForm(ModelForm):
    class Meta:
        model = personal;
        exclude=('primary_table','prn','backlogs','yeardrop','certification','project','academic','extracurricular','workex','Extra_field','last_update')
        widgets = {
                'birthdate' : SelectDateWidget(years = getYears(previousYears=30))
               }

