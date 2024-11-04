

from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from register.choices import EVENT
from register.models import  ChildrenMinistryEvent, Child, ChildImage, Event, EventActivity, OrderOfEvent, Parent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML, Fieldset
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
                 HTML("""<b class="text-dark"> Child's full names</b> <hr>"""),

            Row(
                Column( 'first_name'),
                Column('last_name'),
                Column('middle_name'),
            ),
            HTML("""<b class="text-dark"> Child's Date of birth and Local Church </b> <hr>"""),
            Row(
                Column('date_of_birth'),
                    #    HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>""")),
                Column('local_church')
            ),
            HTML("""<b class="text-dark"> Child's Gender and Talent </b> <hr>"""),
            Row(
                Column(
                     InlineRadios('gender',css_class='form-check'),
                ),
                Column('talent'),
            ),
           

             HTML("""<hr> """),
            FormActions(
                Submit('save', 'Save',css_class='mx-4 px-4 btn btn-success'),
                Submit('save_and_add_another', 'Save and Add Another',css_class=' mx-2 px-4 btn btn-warning text-end'),   
                HTML(""" {% if request.GET.next %} <input type="hidden" name="next" value="{{ request.GET.next }}"/> {% endif %}"""),
            )
        )

# 

class EditRegisterForm(RegisterForm):
    
    def __init__(self, *args, **kwargs):
        super(EditRegisterForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            
            Row(
                Column( 'first_name'),  
                Column('last_name'),
                Column('middle_name'),
            ),
            
            Row(
                Column('date_of_birth',
                       HTML("""<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>""")),
                Column('local_church')
            ),
            Row(
                Column(
                     InlineRadios('gender',css_class='form-check'),
                ),
                Column('talent'),
            ),
             HTML("""<hr> """),
            FormActions(
                Submit('save', 'Save', css_class='mx-4 px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel' ,css_class='mx-4 px-4 btn btn-sm btn-warning')
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

            # display image 
             HTML(""" {% if image.image %} 
                  <div class="text-center">
                    <img
                    style="height: 20rem; width: 20rem; margin: auto; border-radius: 150px"
                    src="{{ image.image.url }}" 
                    /> 
                  </div>
                  {% endif %} """),

            'image',

             HTML("""<hr> """),
            FormActions(
                Submit('save', 'Save', css_class='mx-2 px-4 btn btn-sm btn-success'),

                # cancel data 
                Submit('cancel', 'Cancel' ,css_class='mx-2 px-4 btn btn-sm btn-warning'),
                Submit('proceed', 'Proceed' ,css_class='mx-2 px-4 btn btn-sm btn-warning'),
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
            Row(
                Column('father_name'),
                Column('father_phone_number'),
            ),
            Row(
                Column('mother_name'),
                Column('mother_phone_number'),
            ),
            Row(
                Column(),
                Column('home_county'),
                Column(),


            ),
            HTML("""<hr> """),
            FormActions(
                Submit('save', 'Save', css_class='mx-4 px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel' ,css_class='mx-4  px-4 btn btn-sm btn-warning text-end')
            )
        )


class CalenderEventForm(forms.ModelForm):
    
    class Meta:
        model = ChildrenMinistryEvent
        fields = ("title", "details", "on_date", "slug",)
        widgets = {
            'on_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'datepicker',
                'placeholder':'MM/DD/YYYY'
            }), 
            'details': forms.Textarea(attrs={
                'class': 'form-control form-control-sm bg-light', 'type':"text", 'placeholder':"Your text ...................",
                
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
                         HTML("""<hr> """),

            'details',
                         HTML("""<hr> """),

            FormActions(
                Submit('save', 'Save', css_class='mx-4 px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel', css_class='mx-4 px-4 btn btn-sm btn-warning')
            
        )
        )
  


class EventActivityForm(forms.ModelForm):
    
    class Meta:
        model = EventActivity
        fields = '__all__'
    
      
    def __init__(self,*args,**kwargs):
        super(EventActivityForm,self).__init__(*args, **kwargs)

        self.helper=FormHelper()
        self.helper.form_method="post"
        self.helper.layout=Layout(
          
            # 
            'procession_of_events',

            FormActions(
                Submit('save', 'Save', css_class=' px-4 mx-4 btn btn-sm btn-success'),
                Submit('add_more', 'Add More Events', css_class='px-4 mx-4 btn btn-sm btn-warning')
            )
        )
        for key, value in self.fields.items():
            self.fields['procession_of_events'].help_text ='You can add your day scriptures and day program '



             
class EventForm(forms.ModelForm):
    
    
    class Meta:
        model = Event
        fields = '__all__'
        
        widgets = {
			'event': forms.Select(choices=EVENT),
		}

    def __init__(self, *args, **kwargs) :
        super(EventForm, self).__init__( *args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_method="post"
        self.helper.layout = Layout(
             'calendar',
               "church",
               HTML("""{% if form.errors %}<div class="alert alert-danger" >{{ form.errors }}</div>{% endif %}"""),
           Row(
               
               Column('event'),
               Column('associate'),
               Column('duration'),
           ),
            HTML("""<hr> """),
        
            FormActions(
                Submit('save', 'Save', css_class=' px-4 mx-4 btn btn-sm btn-success'),
                Submit('add_more', 'Add More Events', css_class='px-4 mx-4 btn btn-sm btn-info'),
                HTML("""
                        <a class='px-4 mx-4 btn btn-sm btn-warning' href="{% url 'view_event' calendar.slug %}">Exit</a>
                    """),
                
            ),
        )
        for key, value in self.fields.items():
            self.fields['church'].widget = forms.HiddenInput()
            self.fields['calendar'].widget = forms.HiddenInput()


