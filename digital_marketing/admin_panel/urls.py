from django.urls import path
from . import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('approve/', views.approve_users, name='approve_users'),
    path('users/', views.admin_view_users, name='admin_view_users'),
    path('users/edit/<int:id>/', views.admin_edit_user, name='admin_edit_user'),
    path('users/delete/<int:id>/', views.admin_delete_user, name='admin_delete_user'),
    path('tasks/', views.admin_task_overview, name='admin_task_overview'),
    path('tasks/<int:id>/', views.admin_task_detail, name='admin_task_detail'),
    path('assign-lead-task/', views.assign_lead_task, name='assign_lead_task'),
    path('leaves/', views.leave_approval, name='leave_approval'),
    path('leaves/<int:id>/<str:action>/', views.approve_leave, name='approve_leave'),
    path('attendance/', views.attendance_overview, name='attendance_overview'),

    path('logout/', logout_fn, name='logout_fn')
]