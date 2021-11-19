from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import get_user_model, authenticate, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.db.models import Q
import environ
import pyodbc
import random

#handling environmental variables
env = environ.Env()
environ.Env.read_env()

server = env("PB_SERVER")
database = env("PB_DATABASE")
username = env("PB_USERNAME")
password = env("PB_PASSWORD")
driver = env("PB_DRIVER")

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def GetUsersListView(request):
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
def DeleteUserView(request, id):
    if request.user.id == id:
        return HttpResponse("You can't delete your own account!", status=409)

    user = get_object_or_404(get_user_model(), pk=id)
    user.delete()

    return HttpResponse("User account deleted!")


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def CreateUserView(request):
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
def CreateSuperuserView(request):
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
def EditUserView(request):
    id = request.POST.get('id', -1)
    username = request.POST.get('username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    is_superuser = request.POST.get('is_superuser', '')

    user = get_object_or_404(get_user_model(), pk=id)

    if str(request.user.id) == id and is_superuser.capitalize() != str(request.user.is_superuser):
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


@api_view(['POST'])
def LoginView(request):
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
def LogoutView(request):
    logout(request)
    return HttpResponse("You have ben successfully logged out!")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def CurrentUserView(request):
    data = {
        'username': request.user.username,
        'is_superuser': request.user.is_superuser
    }

    return JsonResponse(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def GetProductsGroupsView(request):
    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=80;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "select grt_Nazwa from sl_GrupaTw where grt_Id in (select distinct tw_IdGrupa from tw__towar);")
            categories = [item[0] for item in cursor.fetchall()]

    return JsonResponse({'groups': categories})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def GetProductsListView(request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 8)
    categories = request.GET.getlist('filteredGroups[]', [])
    search = request.GET.get('search', '')
    order_direction = request.GET.get('order_direction', 'ASC')

    products = []
    random.seed(0)

    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=80;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tw_Nazwa, (SELECT SUM(st_Stan) from tw_stan WHERE st_TowId = tw_Id), tw_Id, (SELECT grt_Nazwa FROM sl_GrupaTw WHERE grt_Id = tw_IdGrupa) as category FROM tw__towar;")
            for row in cursor.fetchall():
                products.append(
                    {
                        'product_name': row[0],
                        'state': int(row[1]),
                        'product_prediction': random.randint(1, 50),
                        'id': row[2],
                        'product_group': row[3]
                    }
                )

    products_processed = []

    for product in products:
        if (product['product_group'] in categories or not categories) and (search.lower() in product['product_name'].lower() or search == ''):
            products_processed.append(product)

    return JsonResponse({'products': products_processed})


# only for development purposes!
@api_view(['GET'])
def CreateInitialSuperuser(request):
    user = get_object_or_404(get_user_model(), username="admin")
    user.delete()
    get_user_model().objects.create_superuser('admin', 'admin', 'admin@example.com', 'admin_f', 'admin_l')
    return HttpResponse("InitialSuperuser created!")
