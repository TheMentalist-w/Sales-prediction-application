from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import get_user_model, authenticate, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.db.models import Q, F, Subquery,OuterRef, Max
from .models import Product, Group, Feature, ProductFeature, Prediction

import environ
import pyodbc

#handling environmental variables
env = environ.Env()
environ.Env.read_env()

server = env("PB_SERVER")
database = env("PB_DATABASE")
username = env("PB_USERNAME")
password = env("PB_PASSWORD")
driver = env("PB_DRIVER")

conn_string = 'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=80;DATABASE=' + database + ';UID=' + username + ';PWD=' + password

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
    groups_names = [{'name':group.name, 'id':group.id} for group in Group.objects.all()]
    return JsonResponse({'groups': groups_names})


@api_view(['GET'])
#@permission_classes((IsAuthenticated, ))
def GetProductsListView(request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 8)
    groups = request.GET.getlist('filteredGroups[]', [])
    characteristics = request.GET.getlist('filteredFeatures[]', [])
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', "-1")

    pr = Prediction(value=5532)
    pr.save()
    Product.objects.get(id=6).predictions.add(pr)

    latest_prediction = Subquery(Prediction.objects.filter(product__id = OuterRef('id'),).order_by("-date").values('value')[:1])

    products = Product.objects.filter((Q(name__icontains=search) | Q(symbol__icontains=search))).annotate(group_name=F('group__name'), prediction =latest_prediction)

    if groups:
        products = products.filter(Q(group__id__in=groups))

    if characteristics:
        products = products.filter(Q(features__id__in=characteristics))

    if sort == "0":
        products = products.order_by("prediction")
    elif sort == "-1":
        products = products.order_by("-prediction")

    products_processed = list(products.values())

    for p in products_processed:
        p["prediction"]=2

    paginator = Paginator(products_processed, size)

    if paginator.num_pages < int(page):
        page = paginator.num_pages

    query_set = [prod for prod in paginator.page(page)]

    return JsonResponse({'products': query_set, 'totalPages': paginator.num_pages, 'page': page})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def GetAvailableFeaturesList(request):

    features_names = [{'name':feature.name, 'id':feature.id} for feature in Feature.objects.all()]
    return JsonResponse({'features': features_names})



@api_view(['GET'])
def CreateInitialSuperuser(request):
    get_user_model().objects.create_superuser('admin', 'admin', 'admin@example.com', 'admin_f', 'admin_l')
    return HttpResponse("InitialSuperuser created!")


def FetchProducts(request):

    #delete all existing products
    #Product.objects.all().delete()

    #download data from PitbullDB and insert new products
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tw_Nazwa, tw_Symbol, "
                           "(SELECT SUM(st_Stan) from tw_stan WHERE st_TowId = tw_Id),"
                           "tw_Id,"
                           "tw_IdGrupa "
                           "FROM tw__Towar;")

            for row in cursor.fetchall():
                Product.objects.update_or_create(name=row[0], symbol=row[1], inventory=int(row[2]), id=int(row[3]), group=Group.objects.get(id=int(row[4])))

    return HttpResponse("Products fetched!")

def FetchGroups(request):
    # delete all existing groups
    #Group.objects.all().delete()

    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("select grt_Id, grt_Nazwa from sl_GrupaTw;")
            for row in cursor.fetchall():
                Group.objects.update_or_create(id=int(row[0]), name=row[1])

    return HttpResponse("Groups fetched!")


def FetchFeaturesDict(request):
    # delete all existing features dict entries
    #Feature.objects.all().delete()

    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT ctw_Id, ctw_Nazwa FROM sl_CechaTw;")
            for row in cursor.fetchall():
                Feature.objects.update_or_create(id=int(row[0]), name=row[1])

    return HttpResponse(f"Features dict fetched!")


def FetchFeaturesDependencies(request):
    # delete all existing product-features dependencies
    #ProductFeature.objects.all().delete()

    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT cht_Id, cht_IdTowar, cht_IdCecha FROM tw_CechaTw;")
            for row in cursor.fetchall():
                product = Product.objects.get(id=int(row[1]))
                feature = Feature.objects.get(id=int(row[2]))
                ProductFeature.objects.update_or_create(id=int(row[0]), product=product, feature=feature)

    return HttpResponse(f"Product-features dependencies fetched!")

def FetchAllData(request):
    FetchGroups(request)
    FetchFeaturesDict(request)
    FetchProducts(request)
    FetchFeaturesDependencies(request)
    return HttpResponse("All data fetched!")
