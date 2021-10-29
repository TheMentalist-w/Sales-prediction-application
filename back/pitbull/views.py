from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from django.contrib.auth import get_user_model, authenticate, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@api_view(['GET'])
@permission_classes((IsAdminUser, )) 
def GetUsersListView(request):
        
        users_data = list(get_user_model().objects.values()) 

        users_prepared = [{
                                'id':i['id'], 
                                'username':i['username'], 
                                'employee':i['first_name'] + " " + i['last_name'],
                                'email':i['email'], 
                                'type': 'Admin' if i['is_staff'] else 'Normal'
                             } for i in users_data
                          ]
        
        return JsonResponse({'users': users_prepared})

@permission_classes((IsAdminUser, )) 
@api_view(['DELETE'])
def DeleteUserView(request,id):
        user = get_object_or_404(get_user_model(), pk = int(id))
        user.delete()

        return HttpResponse("User account deleted!") 

@permission_classes((IsAdminUser, )) 
@api_view(['POST'])
def CreateUserView(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    first_name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')

    user = get_user_model().objects.create_user(
        username = username,
        password = password,
        email = email,
        first_name = first_name,
        last_name = last_name
    )
        
    return JsonResponse({'new_user_id': user.id}) 

@permission_classes((IsAdminUser, )) 
@api_view(['POST'])
def CreateSuperuserView(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    first_name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')

    user = get_user_model().objects.create_superuser(
        username = username,
        password = password,
        email = email,
        first_name = first_name,
        last_name = last_name
    )
    
    return JsonResponse({'new_superuser_id': user.id}) 

@permission_classes((IsAdminUser, )) 
@api_view(['POST'])
def EditUserView(request):

        id = request.POST.get('id',-1)
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        is_staff = request.POST.get('is_staff','')

        user = get_object_or_404(get_user_model(), pk = id)

        if username != '': user.username = username
        if password != '': user.set_password(password)
        if email != '': user.email = email
        if is_staff != '': user.is_staff = is_staff

        user.save()
        
        return HttpResponse("User account edited!")

@api_view(['POST'])
def LoginView(request):

    login_data = request.POST.get('login_data','')
    password = request.POST.get('password','')

    username_result = None
    try:
        validate_email(login_data)
        username_result = authenticate(request, email = login_data, password = password)
    except ValidationError:
        username_result = authenticate(request, username = login_data, password = password)

    if username_result is not None:
        token_data = RefreshToken.for_user(username_result)
        data = {'text':'Login successful!','access': str(token_data.access_token),'refresh':str(token_data)} 
        return JsonResponse(data) 
    else:
        return HttpResponseNotFound("Login failed! User not found or password is incorrect")

@api_view(['POST'])
def LogoutView(request):
    logout(request)
    return HttpResponse("You have ben successfully logged out!")

@permission_classes((IsAuthenticated, )) 
@api_view(['GET'])
def CurrentUserView(request):
    return HttpResponse(request.user.username if request.user.is_authenticated else "Anonymous User")
