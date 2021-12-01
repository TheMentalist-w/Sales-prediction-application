from django.urls import path
from .. import views

users_managing_urlpatterns = [
    # managing users
    path('users/',views.get_users_list, name='getUsersList'),
    path('user/create/',views.create_user, name='createUser'),
    path('user/delete/<int:id>/',views.delete_user, name='deleteUser'),
    path('user/edit/',views.edit_user, name='editUser'),
    path('superuser/create/',views.create_superuser, name='createSuperuser'),

]

