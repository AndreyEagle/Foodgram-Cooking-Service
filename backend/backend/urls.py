from django.contrib import admin
from django.urls import include, path


app_name = 'foodgram'
app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('foodgram.urls')),
]
