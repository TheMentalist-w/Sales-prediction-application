from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView

auth_urlpatterns = [
    # managing authorization
    path('user/logout/', views.logout_user, name='logout'),
    path('user/login/', views.login_user, name='login'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('user/current/', views.get_current_user, name='currentUser'),
]

