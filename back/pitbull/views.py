from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.decorators import api_view

def index(request):
    return HttpResponse("Hello, world. You're at the Pitbull main page")

@api_view(['GET', 'POST', 'DELETE'])
def HandleUsersView(request):

    if request.method == 'GET':    #list all users
        users_data = list(get_user_model().objects.values()) 

        #return only specific fields
        #users_data = [ { key: user[key] for key in ["id","username", "first_name", "last_name","password","email","is_staff"] } for user in users_data]
        users = []
        
        for i in users_data:
            account_type = 'Normal'
            if i['is_staff']:
                account_type = 'Admin'
            users += [{'id':i['id'], 'username':i['username'], 'employee':i['first_name'] + " " + i['last_name'], 'email':i['email'], 'type':account_type}]
        #users_data = [ { key: user[key] for key in ["id","username", "first_name", "last_name","password","email","is_staff"] } for user in users_data]
        return JsonResponse({'users':users})
    
    elif request.method == 'POST':   #create new user
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        get_user_model().objects.create_user(username = username, password = password)
        return HttpResponse("User account created!")
    
    elif request.method == 'DELETE':    #delete desired user
        user = get_user_model().objects.get(username = request.POST['username'])
        user.delete()
        return HttpResponse("User account deleted!") 

@api_view(['POST'])
def CreateSuperuserView(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    get_user_model().objects.create_superuser(username = username, password = password)
    return HttpResponse("Superuser account created!")


@api_view(['POST'])
def LoginView(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    username = authenticate(request, username = username, password = password)
    useremail = authenticate(request, email = username, password = password)
    if username is not None:
        login(request, username)
        # Redirect to a success page. @TODO
        return HttpResponse("Login successful!")
    elif useremail is not None:
        login(request, useremail)
        # Redirect to a success page. @TODO
        return HttpResponse("Login successful!")
    else:
        # Return an 'invalid login' error message. @TODO
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

def CurrentUserView(request):
    return HttpResponse(request.user.username if request.user.is_authenticated else "Anonymous User")
