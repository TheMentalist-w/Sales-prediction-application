from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def get_users_list(request):
    users_data = None

    page = request.GET.get('page', 1)
    size = request.GET.get('size', 8)

    search_keyword = request.GET.get('search', '')

    if search_keyword != '':
        users_data = list(get_user_model().objects.filter(
            Q(first_name__icontains=search_keyword) |
            Q(last_name__icontains=search_keyword) |
            Q(username__icontains=search_keyword) |
            Q(email__icontains=search_keyword)).values()
                          )
    else:
        users_data = list(get_user_model().objects.values())

    paginator = Paginator(users_data, size)
    if paginator.num_pages < int(page):
        page = paginator.num_pages
    query_set = paginator.page(page)
    users_prepared = [{
        'id': i['id'],
        'username': i['username'],
        'first_name': i['first_name'],
        'last_name': i['last_name'],
        'email': i['email'],
        'type': 'Admin' if i['is_superuser'] else 'Normal'
    } for i in query_set
    ]
    return JsonResponse({'users': users_prepared, 'totalPages': paginator.num_pages, 'page': page})


@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def delete_user(request, given_id):
    if request.user.id == given_id:
        return HttpResponse("You can't delete your own account!", status=409)

    user = get_object_or_404(get_user_model(), pk=given_id)
    user.delete()

    return HttpResponse("User account deleted!")


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_user(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')

    if get_user_model().objects.filter(Q(username=username) | Q(email=email)).exists():
        return HttpResponse("User already exists!", status=409)
    else:
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return JsonResponse({'new_user_id': user.id})


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_superuser(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')

    if get_user_model().objects.filter(Q(username=username) | Q(email=email)).exists():
        return HttpResponse("User already exists!", status=409)
    else:
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return JsonResponse({'new_superuser_id': user.id})


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def edit_user(request):
    given_id = request.POST.get('id', -1)
    username = request.POST.get('username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    is_superuser = request.POST.get('is_superuser', '')

    user = get_object_or_404(get_user_model(), pk=given_id)

    if str(request.user.id) == given_id and is_superuser.capitalize() != str(request.user.is_superuser):
        return HttpResponse("Can't change your own account type!", status=409)

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





