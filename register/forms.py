

from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from register.models import  CalenderEvent, Child, ChildImage, EventActivity, Parent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML
from crispy_forms.bootstrap import InlineRadios, FormActions 

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Child
        fields = '__all__' 
        exclude = ('attendance_rate',)
        widgets = {
            'gender': forms.RadioSelect(attrs={"class": "inline li"}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'datepicker',
            }), 

        }
        

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'first_name',
            'middle_name',
            'last_name',
            Row(
                Column('date_of_birth',
                       HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>""")),
                Column('local_church')
            ),
            InlineRadios('gender',css_class='form-check'),
            'talent',
            FormActions(
                Submit('save', 'Save',css_class='px-4 btn btn-success'),
                Submit('save_and_add_another', 'Save and Add Another',css_class=' mx-4 px-4 btn btn-warning text-end'),
                
                HTML(""" {% if request.GET.next %} <input type="hidden" name="next" value="{{ request.GET.next }}"/> {% endif %}"""),
            )
        )

# 

class EditRegisterForm(RegisterForm):
    
    def __init__(self, *args, **kwargs):
        super(EditRegisterForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'first_name',
            'middle_name',
            'last_name',
            Row(
                Column('date_of_birth',
                       HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>""")),
                Column('local_church')
            ),
            InlineRadios('gender',css_class='form-check'),
            'talent',
            FormActions(
                Submit('save', 'Save', css_class='text-center  px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel' ,css_class='text-center  px-4 btn btn-sm btn-warning')
            )
        )


# create image form , this is passed to the views

class ImageForm(forms.ModelForm):
    
    class Meta:
        model = ChildImage
        fields = '__all__'
        exclude=('child',)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args,**kwargs)

        # uses  crispy-form  

        self.helper=FormHelper()
        self.helper.form_method ='post'
        self.helper.layout=Layout(
            'image',
            FormActions(
                Submit('save', 'Save', css_class='mx-4 px-4 btn btn-sm btn-success'),

                # cancel data 
                Submit('cancel', 'Cancel' ,css_class='mx-4 px-4 btn btn-sm btn-warning'),
            )
        )


class ParentForm(forms.ModelForm):
    
    class Meta:
        model = Parent
        fields = '__all__'
        exclude=('child',)

    def __init__(self, *args, **kwargs  ):
        super().__init__(*args, **kwargs)
        self.helper =FormHelper()
        self.helper.form_method= 'post'
        self.helper.layout= Layout(
            'father_name',
            'mother_name',
            Row(
                Column('phone_number'),
                Column('home_county'),

            ),
            FormActions(
                Submit('save', 'Save', css_class='text-center  px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel' ,css_class='  px-4 btn btn-sm btn-warning text-end')
            )
        )


class CalenderEventForm(forms.ModelForm):
    
    class Meta:
        model = CalenderEvent
        fields = ("title", "details", "on_date", "slug",)
        widgets = {
            'on_date': forms.DateInput(attrs={
                'class': 'form-control',
                 'readonly': 'readonly',
                'id': 'datepicker',
            }), 
        }
   

    def __init__(self, *args, **kwargs):
        super(CalenderEventForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('on_date',
                       HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>"""))
            ),
            'details',
            FormActions(
                Submit('save', 'Save', css_class='text-center px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel', css_class='text-center px-4 btn btn-sm btn-warning')
            )
        )
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if CalenderEvent.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A calendar event with this title already exists.")
        return slug


class EventActivityForm(forms.ModelForm):
    
    class Meta:
        model = EventActivity
        fields = ("procession_of_events","days_scripture",)
    
      
    def __init__(self,*args,**kwargs):
        super(EventActivityForm,self).__init__(*args, **kwargs)

        self.helper=FormHelper()
        self.helper.form_method="post"
        self.helper.layout=Layout(
            'days_scripture',
            
            'procession_of_events',

            FormActions(
                Submit('save', 'Save', css_class=' px-4 mx-4 btn btn-sm btn-success'),
                Submit('add_more', 'Add More Events', css_class='px-4 mx-4 btn btn-sm btn-warning')
            )
        )
        for key, value in self.fields.items():
            self.fields['procession_of_events'].help_text ='You can add your day scriptures and day program '
             
                