from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mainPage'),
    path('users/',views.HandleUsers, name='handleUsers'),
]