from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes((IsAdminUser, )) 
def GetUsersListView(request):
        users_data = list(get_user_model().objects.values()) 
        users = []
        
        for i in users_data:
            account_type = 'Normal'
            if i['is_staff']:
                account_type = 'Admin'
            users += [{'id':i['id'], 'username':i['username'], 'employee':i['first_name'] + " " + i['last_name'], 'email':i['email'], 'type':account_type}]
        #users_data = [ { key: user[key] for key in ["id","username", "first_name", "last_name","password","email","is_staff"] } for user in users_data]
        return JsonResponse({'users':users})
        

@api_view(['DELETE'])
def DeleteUserView(request):
        id =  request.POST.get('id')

        user = get_object_or_404(get_user_model(), pk = id)
        user.delete()

        return HttpResponse("User account deleted!") 

@api_view(['POST'])
def CreateUserView(request):
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')

    user = get_user_model().objects.create_user(username = username, password = password, email = email)
        
    return JsonResponse({'new_user_id': user.id}) 

@api_view(['POST'])
def CreateSuperuserView(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = get_user_model().objects.create_superuser(username = username, password = password)
    return JsonResponse({'new_superuser_id': user.id}) 

@api_view(['POST'])
def EditUserView(request):

        id = request.POST.get('id',-1)
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        is_staff = request.POST.get('is_staff','')

        user = get_object_or_404(get_user_model(), pk = id)

        if username != '': user.username = username
        if password != '': user.password = password
        if email != '': user.email = email
        if is_staff != '': user.is_staff = is_staff

        user.save()
        
        return HttpResponse("User account edited!")

@api_view(['POST'])
def LoginView(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')

    username_result = authenticate(request, username = username, password = password)
    useremail_result = authenticate(request, email = username, password = password)
    if username_result is not None:
        login(request, username_result)
        # Redirect to a success page. @TODO
        return HttpResponse("Login successful!")
    elif useremail_result is not None:
        login(request, useremail_result)
        # Redirect to a success page. @TODO
        return HttpResponse("Login successful!")
    else:
        return HttpResponseNotFound("Login failed! User not found or password is incorrect")

@api_view(['POST'])
def DeleteUser(request):
    id = request.POST.get('id','')
    user = get_user_model().objects.get(id=id)
    if user is not None:
        user.delete()
        # Redirect to a success page. @TODO
        return HttpResponse("Deletion successful!")
    else:
        # Return an 'invalid login' error message. @TODO
        return HttpResponseNotFound("Cannot delete user")

@api_view(['POST'])
def NewUser(request):
    #user = get_user_model()
    #user['is_staff'] = request.POST.get('is_staff', '')
    return JsonResponse({'id': 5})
    #user.save()
    #if user.id is not None:
        # Redirect to a success page. @TODO
    #    return JsonResponse({'id': 5})
    #else:
        # Return an 'invalid login' error message. @TODO
    #    return HttpResponseNotFound("Cannot create user")

@api_view(['POST'])
def EditUser(request):
    #user = get_user_model()
    #user['is_staff'] = request.POST.get('is_staff', '')
    return HttpResponse("You have ben successfully logged out!")
    #user.save()
    #if user.id is not None:
        # Redirect to a success page. @TODO
    #    return JsonResponse({'id': 5})
    #else:
        # Return an 'invalid login' error message. @TODO
    #    return HttpResponseNotFound("Cannot create user")

@api_view(['POST'])
def LogoutView(request):
    logout(request)
    return HttpResponse("You have ben successfully logged out!")

@api_view(['GET'])
def CurrentUserView(request):
    return HttpResponse(request.user.username if request.user.is_authenticated else "Anonymous User")
