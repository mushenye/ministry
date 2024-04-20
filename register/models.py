import datetime
from django.db import models
from . choices import CHURCH, GENDER, TALENT, COUNTY
from PIL import Image
# Create your models here.



class Child(models.Model):
    date_created=models.DateField(auto_now_add=True)
    first_name =models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(max_length=100)
    local_church=models.CharField(choices=CHURCH, max_length=100)
    attendance_rate=models.IntegerField(default=1)
    gender=models.CharField(choices=GENDER,max_length=10, default='Boy')
    talent=models.CharField(choices=TALENT,max_length=20, blank=True,null=True)


    def age(self):
        today = datetime.datetime.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def __str__(self):
            return '{} {}' .format(self.first_name, self.last_name)

class ChildImage(models.Model):
    date_created=models.DateField(auto_now_add=True)
    child=models.OneToOneField(Child, on_delete=models.CASCADE)
    image=models.ImageField(max_length=100,upload_to='child_images', blank=True,null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
            return '{} {}' .format(self.child.first_name, self.child.last_name)
    
    
class Parent(models.Model):
    child=models.ForeignKey(Child, on_delete=models.CASCADE)
    father_name=models.CharField(max_length=100,blank=True, null=True)
    mother_name=models.CharField(max_length=100,blank=True, null=True)
    phone_number=models.IntegerField(blank=True, null=True)
    home_county=models.CharField( choices=COUNTY,max_length=20, blank=True, null=True)

    def __str__(self):
        return '{} {}' .format(self.child.first_name, self.child.last_name)


class CalenderEvent (models.Model):
    date_created=models.DateField(auto_now_add=True)
    on_date=models.DateField()
    title=models.CharField(max_length=100)
    details=models.TextField(max_length=500)
    children_attendance = models.ManyToManyField(Child, through='Attendance', related_name='lessons_attended')
    
    def __str__(self):
        return self.title

class Attendance(models.Model):
    date_created=models.DateField(auto_now_add=True)
    activity=models.ForeignKey(CalenderEvent, on_delete=models.CASCADE)
    child_attendance=models.ForeignKey(Child, on_delete=models.CASCADE)
    in_attendance=models.BooleanField(default=False)


    def __str__(self):
        return '{} {}' .format(self.child_attendance.first_name, self.child_attendance.last_name)
    

class EventActivity(models.Model):
     date_created=models.DateField(auto_now_add=True)
     activity=models.ForeignKey(CalenderEvent, on_delete=models.CASCADE)
     church=models.CharField(choices=CHURCH, max_length=20)
     event=models.TextField(max_length=200)
