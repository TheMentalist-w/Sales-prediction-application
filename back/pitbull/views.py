from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

def index(request):
    return HttpResponse("Hello, world. You're at the Pitbull main page")

@api_view(['GET', 'POST', 'DELETE'])
def HandleUsers(request):

    if request.method == 'GET':    #list all users
        users_data = list(get_user_model().objects.values())  
        return JsonResponse({'users': users_data}) 
    
    elif request.method == 'POST':   #create new user
        username, password = request.POST.get('username',''), request.POST.get('password','')
        get_user_model().objects.create_user(username = username, password = password)
        return HttpResponse("User created!")
    
    elif request.method == 'DELETE':    #delete desired user
        user = get_user_model().objects.get(username = request.POST.get('username'))
        user.delete()
        return HttpResponse("User deleted!") 