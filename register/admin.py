from django.contrib import admin

from register.models import Parent,Child,ChildrenMinistryEvent,OrderOfEvent,Event

# Register your models here.
admin.site.register(Parent)
admin.site.register(ChildrenMinistryEvent)
admin.site.register(Child)
admin.site.register(OrderOfEvent)
admin.site.register(Event)