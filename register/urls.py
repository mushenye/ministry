from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add/child/',views.add_child, name='add' ),
    path('view/children/',views.child_view, name='view_child' ),
    # path('view/children/',ChildrenListView.as_view(), name='view_child' ),

    path('view/image/detail/<int:pk>/',views.add_image, name='add_image' ),
    path('view/children/details/<str:slug>',views.view_child_details, name='view_child_details' ),
    path('add/parent/details/<int:pk>',views.add_parent, name='parent' ),
    path('edit/child/details/<str:slug>',views.edit_child_details, name='edit_child' ),
    path('add/calendar/event/',views.create_sunday_activity, name='calendar' ),
    path('view/calender/event/',views.view_events, name='view_events' ),
    path('create/attendance/<str:slug>', views.create_attendance, name='create_attendance' ),
    path('mark-attendance/<int:pk>',views.mark_attendance, name='mark' ),
    path('create-event/<str:slug>',views.create_event, name='create-event' ),






]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header= "Simani Technologies"
admin.site.site_title= "Simani Technologies"
admin.site.site_index_title = "welcome to simani technologies"