from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView

auth_urlpatterns = [
    # managing authorization
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('current/', views.get_current_user, name='currentUser'),
]

