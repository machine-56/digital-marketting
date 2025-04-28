from django.urls import path
from .import views
from accounts.views import logout_fn

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.exc_home, name='exc_home'),
    path('leads/', views.view_leads, name='view_leads'),
    
    path('attendance/', views.mark_attendance_and_apply_leave, name='mark_attendance_and_apply_leave'),
    path('change-password/', views.exc_change_password, name='exc_change_password'),

    path('logout/', logout_fn, name='logout_fn')

]