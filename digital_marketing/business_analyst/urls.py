from django.urls import path
from . import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.ba_home, name='ba_home'),
    path('tasks/', views.ba_task_list, name='ba_task_list'),
    path('tasks/<int:task_id>/', views.ba_task_detail, name='ba_task_detail'),
    path('tasks/<int:task_id>/add-report/', views.add_daily_report, name='add_daily_report'),
    path('tasks/<int:task_id>/submit/', views.submit_task, name='submit_task'),

    path('logout/', logout_fn, name='logout_fn')

]