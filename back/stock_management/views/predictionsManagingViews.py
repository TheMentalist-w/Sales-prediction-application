from django.http import JsonResponse
from ..models import Place
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


