from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.decorators import api_view
#from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the Pitbull main page")

@api_view(['GET', 'POST', 'DELETE'])
def HandleUsersView(request):

    if request.method == 'GET':    #list all users
        users_data = list(get_user_model().objects.values())  
        return JsonResponse({'users': users_data}) 
    
    elif request.method == 'POST':   #create new user
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        get_user_model().objects.create_user(username = username, password = password)
        return HttpResponse("User created!")
    
    elif request.method == 'DELETE':    #delete desired user
        user = get_user_model().objects.get(username = request.POST['username'])
        user.delete()
        return HttpResponse("User deleted!") 

@api_view(['POST'])
def LoginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page. @TODO
        return HttpResponse("Login successful!")
    else:
        # Return an 'invalid login' error message. @TODO
        return HttpResponseNotFound("Login failed! User not found or password is incorrect")

@api_view(['POST'])
def LogoutView(request):
    logout(request)
    return HttpResponse("You have ben successfully logged out!")

def CurrentUserView(request):
    return HttpResponse(request.user.username if request.user.is_authenticated else "Anonymous User")
