from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('endpoints/', include('endpoints.urls')),
    path('admin/', admin.site.urls),
]