from django.urls import path
from .import views 
from accounts.views import logout_fn

urlpatterns = [
    path('', views.dma_home, name='dma_home'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('view-executives/', views.view_executives, name='view_executives'),
    path('assign-leads/<int:executive_id>/', views.assign_leads, name='assign_leads'),
    path('upload-leads/', views.upload_leads, name='upload_leads'),
    path('view-leads/', views.dma_view_leads, name='dma_view_leads'),
    path('attendance/', views.dma_mark_attendance_and_apply_leave, name='dma_mark_attendance_and_apply_leave'),
    path('change-password/', views.change_password, name='change_password'),

    path('logout/', logout_fn, name='logout_fn')

]