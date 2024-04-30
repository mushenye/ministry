from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm

from django.contrib.auth.models import User

from user.models import CustomUser

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Row, Column, HTML
from crispy_forms.bootstrap import InlineRadios, FormActions 


class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label='old Password',widget= forms.PasswordInput(attrs={'autofocus': 'True','autocomplete':'current-password','class': 'form-control'}))
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email','local_church','phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout=Layout(
            Row(
                Column ('username'),
                Column ('email'),
            ),
            Row(
                Column('local_church'),
                Column('phone_number'),
            ),
            
            'password1',
            'password2',
             FormActions(
                Submit('save', 'Save', css_class='text-center  px-4 btn btn-sm btn-success'),
                Submit('cancel', 'Cancel' ,css_class='  px-4 btn btn-sm btn-warning text-end'),
            )

        )
     

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout= Layout(
            'username',
            'password',
             FormActions(
                Submit('Login', 'Login', css_class='mx-5 px-4 btn btn-sm btn-success'),
                
            )

        )