import datetime
from django.db import models

from user.models import CustomUser
from . choices import CHURCH, EVENT, GENDER, TALENT, COUNTY
from PIL import Image
from django.template.defaultfilters import slugify
import uuid
# Create your models here.



class Child(models.Model):
    date_created=models.DateField(auto_now_add=True)
    first_name =models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(max_length=100)
    local_church=models.CharField(choices=CHURCH, max_length=100)
    attendance_rate=models.IntegerField(default=0)
    gender=models.CharField(choices=GENDER,max_length=10, default='Boy')
    talent=models.CharField(choices=TALENT,max_length=20, blank=True,null=True)
    slug=models.SlugField(blank=True, null=True, unique=True)

    def get_slug_string(self):
        elements = [self.first_name, self.middle_name, self.last_name]
        filtered_elements = filter(None, elements)
        return ' '.join(filtered_elements)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.get_slug_string())
            self.slug = base_slug
            if Child.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        return super().save(*args, **kwargs)


    def age(self):
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def __str__(self):
            return '{} {}' .format(self.first_name, self.last_name)
    
    
    def rate (self):
        calendar=ChildrenMinistryEvent.objects.filter(is_on_date=True).count()
        percent_rate= (self.attendance_rate/calendar)*100
        return round(percent_rate)

    


    

# model for child image

class ChildImage(models.Model):
    date_created=models.DateField(auto_now_add=True)
    child=models.OneToOneField(Child, on_delete=models.CASCADE)
    image=models.ImageField(max_length=100,upload_to='child_images', blank=True,null=True)

    # save fuction ensure the image size is minimized , avoid 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    # 
    def __str__(self):
            return '{} {}' .format(self.child.first_name, self.child.last_name)
    
    
class Parent(models.Model):
    child=models.ForeignKey(Child, on_delete=models.CASCADE)
    father_name=models.CharField(max_length=100,blank=True, null=True)
    father_phone_number=models.IntegerField(blank=True, null=True)
    mother_name=models.CharField(max_length=100,blank=True, null=True)
    mother_phone_number=models.IntegerField(blank=True, null=True)
    home_county=models.CharField( choices=COUNTY,max_length=20, blank=True, null=True)

    def __str__(self):
        return '{} {}' .format(self.child.first_name, self.child.last_name)


class ChildrenMinistryEvent (models.Model):
    date_created=models.DateField(auto_now_add=True)
    slug=models.SlugField(blank=True, null=True, unique=True)
    on_date=models.DateField()
    title=models.CharField(max_length=100)
    details=models.TextField(max_length=50)
    children_attendance = models.ManyToManyField(Child, through='Attendance', related_name='lessons_attended')
    is_on_date=models.BooleanField(default=False)
   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug=slugify(self.title)
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title



class Attendance(models.Model):
    date_created=models.DateField(auto_now_add=True, )
    activity=models.ForeignKey(ChildrenMinistryEvent, on_delete=models.CASCADE)
    child=models.ForeignKey(Child, on_delete=models.CASCADE)
    in_attendance=models.BooleanField(default=False)


    def __str__(self):
        return '{} {}' .format(self.child.first_name, self.child.last_name)
    

class Event(models.Model):
    calendar=models.ForeignKey(ChildrenMinistryEvent, on_delete=models.CASCADE)
    church=models.CharField(max_length=20)
    date_created=models.DateField(auto_now=True)
    event=models.CharField(choices=EVENT, max_length=100)
    associate=models.CharField(max_length=100, default=None)
    duration=models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.event}- {self.associate}"
    




class OrderOfEvent(models.Model):
    local_church=models.CharField(max_length=20)
    calendar=models.ForeignKey(ChildrenMinistryEvent, on_delete=models.CASCADE)
    date_created=models.DateField(auto_now_add=True)
    events=models.ManyToManyField(Event, through ="EventActivity", related_name="events", )
  

    def __str__(self):
        return f"{self.calendar.title}- {self.local_church}"     

    

class EventActivity(models.Model):
    order_of_events=models.ForeignKey(OrderOfEvent, on_delete=models.CASCADE)
    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    



    def __str__ (self):
         return self.event.event 
