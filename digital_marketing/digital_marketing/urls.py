from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('ad/', include('admin_panel.urls')),
    path('ba/', include('business_analyst.urls')),
    path('dm/', include('DM_analyst.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
