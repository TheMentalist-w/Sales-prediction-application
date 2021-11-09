from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from django.contrib.auth import get_user_model, authenticate, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.db.models import Q

@api_view(['GET'])
@permission_classes((IsAdminUser, )) 
def GetUsersListView(request):
        
        users_data = None

        page = request.GET.get('page',1)
        size = request.GET.get('size',8)
        
        search_keyword = request.GET.get('search','')
        
        if search_keyword != '':
            users_data = list(get_user_model().objects.filter(
                Q(first_name__icontains = search_keyword) |
                Q(last_name__icontains = search_keyword) |
                Q(username__icontains = search_keyword) |
                Q(email__icontains = search_keyword)).values()
            )
        else:
            users_data = list(get_user_model().objects.values())
        
        paginator = Paginator(users_data, size)
        if paginator.num_pages < int(page):
            page = paginator.num_pages
        query_set = paginator.page(page)
        users_prepared = [{
                                'id':i['id'],
                                'username':i['username'],
                                'first_name':i['first_name'],
                                 'last_name':i['last_name'],
                                'email':i['email'],
                                'type': 'Admin' if i['is_superuser'] else 'Normal'
                            }  for i in query_set
                         ]
        return JsonResponse({'users': users_prepared, 'totalPages': paginator.num_pages, 'page': page})


@api_view(['DELETE'])
@permission_classes((IsAdminUser, )) 
def DeleteUserView(request,id):
        user = get_object_or_404(get_user_model(), pk = id)
        user.delete()

        return HttpResponse("User account deleted!") 


@api_view(['POST'])
@permission_classes((IsAdminUser, )) 
def CreateUserView(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    first_name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')

    if get_user_model().objects.filter( Q(username = username) | Q(email = email) ).exists():
        return HttpResponse("User already exists!",status = 409)
    else:
        user = get_user_model().objects.create_user(
            username = username,
            password = password,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        return JsonResponse({'new_user_id': user.id}) 

@api_view(['POST'])
@permission_classes((IsAdminUser, )) 
def CreateSuperuserView(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    first_name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')

    if get_user_model().objects.filter( Q(username = username) | Q(email = email) ).exists():
        return HttpResponse("User already exists!",status = 409)
    else:
        user = get_user_model().objects.create_superuser(
            username = username,
            password = password,
            email = email,
            first_name = first_name,
            last_name = last_name
        )
    
        return JsonResponse({'new_superuser_id': user.id}) 


@api_view(['POST'])
@permission_classes((IsAdminUser, )) 
def EditUserView(request):

        id = request.POST.get('id',-1)
        username = request.POST.get('username','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        is_superuser = request.POST.get('is_superuser','')

        user = get_object_or_404(get_user_model(), pk = id)

        if username != '': user.username = username
        if first_name != '': user.first_name = first_name
        if last_name != '': user.last_name = last_name
        if email != '': user.email = email
        if password != '':
            print(password)
            user.set_password(password)
        if is_superuser == 'true': 
            user.is_superuser = True
            user.is_staff = True
        elif is_superuser == 'false':
            user.is_superuser = False
            user.is_staff = False

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

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def CurrentUserView(request):

    data = {
        'username' : request.user.username,
        'is_superuser' :  request.user.is_superuser
    }

    return JsonResponse(data)
