import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from register.choices import CHURCH
from register.forms import  CalenderEventForm, EditRegisterForm, EventActivityForm, ImageForm, ParentForm, RegisterForm
from register.models import Attendance, CalenderEvent, Child, ChildImage, Parent

# Create your views here.

def index(request):
    return render(request, 'register/home.html')

def add_child(request):
    if request.method =="POST":
        form =RegisterForm(request.POST)
        if form.is_valid():


            child=form.save()
            ChildImage.objects.create(child=child)
            Parent.objects.create(child=child)
            if "save_and_add_another" in request.POST:
                
                return redirect('add')
            
            elif 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('view_child_details',child.slug)
    else:
        form=RegisterForm()

    return render(request, 'register/add_child.html', {'form':form})



def edit_child_details(request,slug):
    child=Child.objects.get(slug=slug)
    if request.method =="POST":
        form =EditRegisterForm(request.POST, instance=child)
        if form.is_valid():
            
            form.save(commit=False)
            if 'cancel' in request.POST:
                messages.warning(request, "No Data added Try again !! ")
                return redirect('view_child_details', slug)

            else:
                form.save()
                messages.success(request, "Data updated successfully!")
                return redirect('view_child_details', child.slug)
           
    else:
        form=EditRegisterForm(instance=child)

    return render(request, 'register/add_child.html', {'form':form})
    





# Fuction add image 
def add_image(request, pk):
    # try block check if unknow pk value is passed to the function 
    try:
        image = ChildImage.objects.get(id=pk)

    except ChildImage.DoesNotExist:
        messages.error(request, "Specified image not found.")
        return redirect('home')  

    # check if its a post request.
    if request.method == "POST":
        
        form = ImageForm(request.POST, request.FILES, instance=image)

        # validate the form 
        if form.is_valid():
            #try block  catches errors that may arise when saving data to the data base 
            try:    
                form.save(commit=False)

                # if cancel, data will not be saved 

                if 'cancel' in request.POST:

                    messages.warning(request, "No image added Try again !! ")
                    return redirect('view_child_details', image.child.slug)
                
                else:
                    # if sunmit doesn't contain cancel , data is saved and redirected 
                    form.save()
                    messages.success(request, "Image updated successfully!")
                    return redirect('view_child_details', image.child.slug)
            except Exception as e:  
                messages.warning(request, f"Failed to update image. Error: {str(e)}")
                return redirect('view_child_details', image.child.slug)
    else:
        #creates instance of image for a particular child 
        # the instance was created during child registration
        # ImageForm  created in form.py
        form = ImageForm(instance=image)

        # render to display 

    return render(request, 'register/add_image.html', {'form': form, 'image':image})


    

def child_view(request):
    churches = CHURCH  
    query = request.GET.get("local_code")
    page_number = request.GET.get("page")
    current_count=0
    if query:
        children = Child.objects.filter(local_church=query)
        current_count = children.count() 
    else:
        children = Child.objects.all()
    
    paginator = Paginator(children, 8) 
    try:
        page_obj = paginator.page(page_number)  
    except PageNotAnInteger:
        page_obj = paginator.page(1)  
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  

    total = Child.objects.all().count()  


    if total > 0:
        percent = int((current_count / total) * 100)
    else:
        percent = 0  # Avoid divide by zero if no children exist at all
    
    return render(request, 'register/view.html', {
        'percent': percent,
        'page_obj': page_obj,
        'churches': churches,
        'count': current_count,
        'query': query,
        'total': total
    })




def view_child_details(request, slug):
    child=Child.objects.get(slug=slug)
    child_image=ChildImage.objects.get(child=child)
   
    child_details=ChildImage.objects.get(child=child)

    parent=Parent.objects.get(child=child)

        
    return render(request, 'register/child_details.html',
                  {'child_details':child_details, 'parent':parent,'child_image':child_image})  



def add_parent(request,pk):
    parent=Parent.objects.get(id=pk)
    if request.method=="POST":
        form=ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save(commit=False)
            if 'cancel' in request.POST:
                messages.warning(request, "Your data not Updated ")
                return redirect('view_child_details', parent.child.slug)
            
            else:
                form.save()
                messages.success(request, 'Data updated successfully ')
                return redirect('view_child_details', parent.child.slug)
    else:
        form=ParentForm(instance=parent)

    return render(request, 'register/parent_add.html', {'form':form, 'parent':parent})




def create_sunday_activity(request):
    
    if request.method== "POST":
        form=CalenderEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_events')
    else:
        form= CalenderEventForm()
    return render(request, 'register/sunday_activity.html', {'form':form})


def view_events(request):
    calender_events=CalenderEvent.objects.all().order_by('-on_date')
    paginator = Paginator(calender_events, 4)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'register/calender_events.html',
                  {'calender_events':calender_events, 'page_obj':page_obj})


def create_attendance(request,slug):
    user=request.user
    if user.is_authenticated:
        calendar_event=CalenderEvent.objects.get(slug=slug)
        children=Child.objects.filter(local_church=user.local_church)
        for child in children:
            Attendance.objects.get_or_create(activity=calendar_event, child=child)
        
        attendance =Attendance.objects.filter(activity=calendar_event)

       
        total_child=attendance.count() 
        present=attendance.filter(in_attendance=True).count()
        absent=total_child-present
        rate=int(present/total_child *100)
        value= (present/total_child)*360

        return render( request,'register/attendance.html' , {
                'attendance':attendance,
                'value':value,
                'rate':rate, 
                'absent':absent,
                'present':present,
                'total_child' :total_child,
                'calendar_event':calendar_event,
    
                })
    else:
        messages.warning(request, 'You are not logged in ')
        return redirect('view_events')





def mark_attendance(request, pk):
   
    attendance = Attendance.objects.get(id=pk)

    today = datetime.date.today()
    activity_date = attendance.activity.on_date

    if today == activity_date:
        attendance.activity.is_on_date = True
        attendance.activity.save()

        if attendance.in_attendance:
            attendance.in_attendance = False
        else:
            attendance.in_attendance = True
            attendance.child.attendance_rate += 1  

        attendance.save()
        attendance.child.save()  
    else:
        
        messages.warning(request, "You are not allowed to mark the attendance on this date.")

    return redirect('create_attendance', attendance.activity.slug)
    

    
    

def create_event(request, slug):
    
    calendar =CalenderEvent.objects.get(slug=slug)
    if request.method =="POST":
        form =EventActivityForm(request.POST)
        if form.is_valid():
            event=form.save(commit=False)
            event.activity=calendar
            event.save()

            if "add_more" in request.POST:
                return redirect('create-event', calendar.slug)
            
            else:
                return redirect('create_attendance',calendar.slug)
            
    else:
        form=EventActivityForm()

    return render(request,'register/event.html', {'form':form,'calendar':calendar})

