from django.contrib import admin
from django.urls import path, include

# for use media(images)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
]

# for use media(images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This is for production deployment for using static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)