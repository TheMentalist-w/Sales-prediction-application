from django.urls import path

from . import views
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('', views.index, name='mainPage'),
    path('users/',views.HandleUsersView, name='handleUsers'),
    path('users/current',views.CurrentUserView, name='currentUser'),
    path('superuser/',views.CreateSuperuserView, name='superUser'),
    path('login/',views.LoginView, name='login'),
    path('logout/',views.LogoutView, name='logout'),
    path('apiDocs/', get_swagger_view(title='Pitbull API'))
]