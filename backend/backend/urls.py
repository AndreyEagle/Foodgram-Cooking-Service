from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

app_name = 'foodgram'
app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('foodgram.urls')),
]

if settings.DEBUG:
    urlpatterns = (
        urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
