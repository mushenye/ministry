

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from user import views as user_views
from user.forms import MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
from user.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),

    # path('mode/<int:pk>/tracer',user_views.mode, name='mode' ),
    # path('level/<int:pk>/tracer',user_views.level, name='level' ),
    # path('online/myname/<int:pk>/search_name',user_views.search_name, name='my_name'),
    # path('normal/myname/<int:pk>/search_name_for/normal',user_views.search_name_normal, name='normal'),
    # path('online/verify/<int:pk>',user_views.verify_online, name='verify_online' ),
    # path('self/registration/',user_views.self_registration, name='self-register' ),

    # path('tracer/delete/<int:pk>/tracer',user_views.delete_tracer, name='tracer_delete' ),

    path('register/',user_views.register, name='register' ),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    # path('accounts/login/',auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),



    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='user/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='user/changepassworddone.html' ),name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page ='login'), name='logout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html', form_class= MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),


]