from django import forms

# Create your forms here.

class JobPostingForm(forms.Form):
    walkin=(('y','yes'),('n','no'));
    company_name=forms.CharField(max_length=50);
    company_url=forms.CharField(max_length=50);
    profile=forms.CharField(widget=forms.Textarea);
    walk_in=forms.ChoiceField(choices=walkin,widget=forms.CheckboxInput(attrs={'onchange':'a(this);'}));
    #how_to_apply=forms.CharField(widget=forms.Textarea)

