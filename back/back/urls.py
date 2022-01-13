from django.urls import include,path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('stock_management/', include('stock_management.urls')),
    path('user_authorization/', include('user_authorization.urls')),
    path('docs/', get_swagger_view(title='PitbullAPI')),
]
