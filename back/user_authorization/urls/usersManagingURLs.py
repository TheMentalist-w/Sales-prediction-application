from django.urls import path
from .. import views

users_managing_urlpatterns = [
    # managing users' models
    path('',views.get_users_list, name='getUsersList'),
    path('create/',views.create_user, name='createUser'),
    path('delete/<int:id>/',views.delete_user, name='deleteUser'),
    path('edit/',views.edit_user, name='editUser'),
    path('superuser/create/',views.create_superuser, name='createSuperuser'),
    path('superuser/init/', views.create_initial_superuser, name='createInitialSuperuser'),
]

