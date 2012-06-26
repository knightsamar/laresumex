from django.forms import ModelForm

from student_info.models import marks

class MarksForm(ModelForm):
    class Meta:
        model = marks;
        exclude = ('primary_table')

