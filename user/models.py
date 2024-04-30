from django.db import models
from django.contrib.auth.models import AbstractUser

from register.choices import CHURCH


class CustomUser(AbstractUser):
    local_church=models.CharField(choices=CHURCH, max_length=100)
    phone_number=models.IntegerField()


