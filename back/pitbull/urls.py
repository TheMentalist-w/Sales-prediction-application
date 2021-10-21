from django.urls import path

from . import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/',views.GetUsersListView, name='getUsersList'),
    path('user/create/',views.CreateUserView, name='createUser'),
    path('user/delete/',views.DeleteUserView, name='deleteUser'),
    path('user/edit/',views.EditUserView, name='editUser'),
    path('user/current/',views.CurrentUserView, name='currentUser'),
    path('superuser/create/',views.CreateSuperuserView, name='createSuperuser'),
    path('user/login/',views.LoginView, name='login'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('user/logout/',views.LogoutView, name='logout'),
    path('docs/', get_swagger_view(title='PitbullAPI')),
    
]