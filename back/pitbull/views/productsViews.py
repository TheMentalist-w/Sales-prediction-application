from django.core.paginator import Paginator
from django.db.models import Q, F, Subquery, OuterRef
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..models import Product, Group, Feature, Prediction


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products_groups(request):
    groups_names = [{'name':group.name, 'id':group.id} for group in Group.objects.all()]
    return JsonResponse({'groups': groups_names})



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products_list(request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 8)
    groups = request.GET.getlist('filteredGroups[]', [])
    characteristics = request.GET.getlist('filteredFeatures[]', [])
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', "-1")

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

    paginator = Paginator(products_processed, size)

    if paginator.num_pages < int(page):
        page = paginator.num_pages

    query_set = [prod for prod in paginator.page(page)]

    return JsonResponse({'products': query_set, 'totalPages': paginator.num_pages, 'page': page})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_available_features(request):

    features_names = [{'name':feature.name, 'id':feature.id} for feature in Feature.objects.all()]
    return JsonResponse({'features': features_names})