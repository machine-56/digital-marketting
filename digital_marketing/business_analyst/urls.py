from django.urls import path
from . import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.ba_home, name='ba_home'),
    path('tasks/', views.ba_task_list, name='ba_task_list'),
    path('tasks/<int:task_id>/', views.ba_task_detail, name='ba_task_detail'),
    path('tasks/<int:task_id>/add-report/', views.add_daily_report, name='add_daily_report'),
    path('tasks/<int:task_id>/submit/', views.submit_task, name='submit_task'),
    path('attendance/', views.ba_mark_attendance_and_apply_leave, name='ba_mark_attendance_and_apply_leave'),
    path('change-password/', views.ba_change_password, name='ba_change_password'),


    path('logout/', logout_fn, name='logout_fn')

]