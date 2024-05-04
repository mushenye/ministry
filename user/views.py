from django.shortcuts import  redirect, render
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

from user.forms import  RegistrationForm


# Create your views here.
# registration form
def register(request):
    if request.method== 'POST':
         form= RegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             messages.success(request,f"Welcome {username} !! Your Account has been created  Succesfully. Log in to continue enjoying our services ")
             return redirect('login')
    else:
        form= RegistrationForm()
    return render(request,'user/register.html',{'form':form})



class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'user/login.html'

    


   
    

