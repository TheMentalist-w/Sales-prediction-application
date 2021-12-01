from django.urls import path
from rest_framework_swagger.views import get_swagger_view

documentation_urlpatterns = [

    # documentation
    path('docs/', get_swagger_view(title='PitbullAPI')),

]

