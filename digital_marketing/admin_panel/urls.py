from django.urls import path
from . import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('approve/', views.approve_users, name='approve_users'),

    path('logout/', logout_fn, name='logout_fn')
]