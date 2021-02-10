from django.urls import path

from endpoints import views

urlpatterns = [
    path('', views.index, name='index'),
]