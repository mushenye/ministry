from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from register.choices import CHURCH, EDUCATION
from PIL import Image
from django.template.defaultfilters import slugify
import uuid

class CustomUser(AbstractUser):
    local_church=models.CharField(choices=CHURCH, max_length=100, blank=True, null=True)
    phone_number=PhoneField(blank=True, null=True ,help_text='Contact phone number')
    
   
        

class Person(models.Model):
    date_created=models.DateField(auto_now_add=True)
    first_name =models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100)
    gender=models.CharField(choices=[('Male','Male'),('Female','Female')],max_length=10, default='Male')
    education_level=models.CharField(choices=EDUCATION,max_length=50)
    slug=models.SlugField(blank=True, null=True, unique=True)
    is_verified=models.BooleanField(default=False)

    def get_slug_string(self):
        elements = [self.first_name, self.middle_name, self.last_name]
        filtered_elements = filter(None, elements)
        return ' '.join(filtered_elements)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.get_slug_string())
            self.slug = base_slug
            if Person.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        return super().save(*args, **kwargs)


    def __str___(self):
        return f"{self.first_name} {self.last_name}"

