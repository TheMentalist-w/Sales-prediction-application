from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mainPage'),
    path('users/',views.HandleUsersView, name='handleUsers'),
    path('users/current',views.CurrentUserView, name='currentUser'),
    path('login/',views.LoginView, name='login'),
    path('logout/',views.LogoutView, name='logout'),
]