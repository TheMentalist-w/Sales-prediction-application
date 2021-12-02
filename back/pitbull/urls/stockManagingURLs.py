from django.urls import path
from .. import views

stock_managing_urlpatterns = [
    # managing products, groups and features
    path('products/', views.get_products_list, name='getProductsList'),
    path('products/groups/', views.get_products_groups, name='getProductsGroups'),
    path('products/features/', views.get_available_features, name='getAvailableFeatures'),
    path('init/superuser/', views.create_initial_superuser, name='createInitialSuperuser'),
]

