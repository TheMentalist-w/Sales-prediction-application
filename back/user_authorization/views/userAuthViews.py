from django.contrib.auth import authenticate, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def login_user(request):

    login_data = request.POST.get('login_data', '')
    password = request.POST.get('password', '')

    username_result = None
    try:
        validate_email(login_data)
        username_result = authenticate(request, email=login_data, password=password)
    except ValidationError:
        username_result = authenticate(request, username=login_data, password=password)

    if username_result is not None:
        token_data = RefreshToken.for_user(username_result)
        data = {'text': 'Login successful!', 'access': str(token_data.access_token), 'refresh': str(token_data)}
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Login failed! User not found or password is incorrect")


@api_view(['POST'])
def logout_user(request):

    logout(request)
    return HttpResponse("You have ben successfully logged out!")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_current_user(request):

    data = {
        'username': request.user.username,
        'is_superuser': request.user.is_superuser
    }

    return JsonResponse(data)