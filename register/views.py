from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from register.forms import  CalenderEventForm, EditRegisterForm, ImageForm, ParentForm, RegisterForm
from register.models import Attendance, CalenderEvent, Child, ChildImage, Parent

# Create your views here.

def index(request):
    return render(request, 'register/home.html')

def add_child(request):
    if request.method =="POST":
        form =RegisterForm(request.POST)
        if form.is_valid():
            child=form.save()
            if "save_and_add_another" in request.POST:
                ChildImage.objects.create(child=child)
                Parent.objects.create(child=child)
                return redirect('add')
            else:
                ChildImage.objects.create(child=child)
                Parent.objects.create(child=child)
                return redirect('view_child_details',child.id)
    else:
        form=RegisterForm()

    return render(request, 'register/add_child.html', {'form':form})



def edit_child_details(request,pk):
    child=Child.objects.get(id=pk)
    if request.method =="POST":
        form =EditRegisterForm(request.POST, instance=child)
        if form.is_valid():
            
            form.save(commit=False)
            if 'cancel' in request.POST:
                messages.warning(request, "No Data added Try again !! ")
                return redirect('view_child_details', pk=child.id)
            
            else:
                form.save()
                messages.success(request, "Data updated successfully!")
                return redirect('view_child_details', pk=child.id)
           
    else:
        form=EditRegisterForm(instance=child)

    return render(request, 'register/edit_child.html', {'form':form})
    



def add_image(request, pk):
    try:
        image = ChildImage.objects.get(id=pk)
    except ChildImage.DoesNotExist:
        messages.error(request, "Specified image not found.")
        return redirect('')  # Assuming 'index' is a sensible fallback view

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            try:
                
                form.save(commit=False)
                if 'cancel' in request.POST:
                    messages.warning(request, "No image added Try again !! ")
                    return redirect('view_child_details', pk=image.child.id)
                
                else:
                    form.save()
                    messages.success(request, "Image updated successfully!")
                    return redirect('view_child_details', pk=image.child.id)
            except Exception as e:  
                messages.warning(request, f"Failed to update image. Error: {str(e)}")
                return redirect('view_child_details', pk=image.child.id)
    else:
        form = ImageForm(instance=image)

    return render(request, 'register/add_image.html', {'form': form})






def view_children(request):
    children=Child.objects.all()
    paginator = Paginator(children, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'register/view.html', context={
        'page_obj':page_obj
    })


def view_child_details(request,pk):
    child=Child.objects.get(id=pk)
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
                return redirect('view_child_details', parent.child.id)
            
            else:
                form.save()
                messages.success(request, 'Data updated successfully ')
                return redirect('view_child_details', parent.child.id)
    else:
        form=ParentForm(instance=parent)

    return render(request, 'register/parent_add.html', {'form':form})




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


def create_attendance(request,pk):
    calender_event=CalenderEvent.objects.get(id=pk)
    children=Child.objects.all()
    for child in children:
        Attendance.objects.get_or_create(activity=calender_event, child=child.id)

    return redirect()



def mark_attendance(request, pk):
    calender_event=CalenderEvent.objects.get(id=pk)
    attendance=Attendance.objects.filter(activity=calender_event)
    


