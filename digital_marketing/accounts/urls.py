from django.urls import path
from .import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login_fn, name='login_fn'),
    path('register/', views.register_fn, name='register_fn'),

    path('logout/', views.logout, name='logout'),
    path('verify/', views.verify_field, name='verify_field'),
]