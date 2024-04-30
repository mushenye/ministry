from django.contrib import admin

from register.models import Parent,CalenderEvent,Child

# Register your models here.
admin.site.register(Parent)
admin.site.register(CalenderEvent)
admin.site.register(Child)