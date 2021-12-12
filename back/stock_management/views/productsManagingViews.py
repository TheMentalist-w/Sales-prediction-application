from django.core.paginator import Paginator
from django.db.models import Q, F, Subquery, OuterRef
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Product, Group, Feature, Prediction, Place


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

    products = Product.objects.filter((Q(name__icontains=search) | Q(symbol__icontains=search))).annotate(group_name=F('group__name'), latest_prediction =latest_prediction)

    if groups:
        products = products.filter(Q(group__id__in=groups))

    if characteristics:
        products = products.filter(Q(features__id__in=characteristics))

    if sort == "0":
        products = products.order_by("latest_prediction")
    elif sort == "-1":
        products = products.order_by("-latest_prediction")

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


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_available_places(request):

    shops = [ {'id': place.id, 'name': place.name} for place in Place.objects.all()]

    return JsonResponse({'shops': shops})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_product_details(request, id):

    prod = get_object_or_404(Product, id=id)

    return JsonResponse({'symbol': prod.symbol,
                         'name': prod.name,
                         'inventory': prod.inventory,
                         'group': prod.group.name,
                         'features' : [{'id': feature.id, 'name': feature.name} for feature in prod.features.all()]})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_product_prediction_history(request):
    prod_id = request.GET.get('productId', -1)
    palce_id = request.GET.get('shopId', -1)

    product = get_object_or_404(Product, id=prod_id)
    place = get_object_or_404(Place, id=palce_id)

    predictions = [[pred.date.strftime('%Y-%m-%d'), pred.value] for pred in Prediction.objects.filter(product=product, place=place)]

    return JsonResponse({'history': predictions})