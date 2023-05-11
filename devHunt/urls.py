from django.contrib import admin
from django.urls import path, include

# for use media(images)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls'))
]

# for use media(images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)