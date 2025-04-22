from django.urls import path
from . import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.dma_home, name='dma_home'),

    path('logout/', logout_fn, name='logout_fn')

]