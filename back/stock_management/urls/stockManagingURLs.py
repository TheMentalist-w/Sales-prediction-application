from django.urls import path
from .. import views

stock_managing_urlpatterns = [
    # managing products, groups and features
    path('products/', views.get_products_list, name='getProductsList'),
    path('products/groups/', views.get_products_groups, name='getProductsGroups'),
    path('products/features/', views.get_available_features, name='getAvailableFeatures'),
    path('shops/', views.get_available_warehouses, name='getAvailableWarehouses'),
    path('product/<int:id>/', views.get_product_details, name='getProductDetails'),
    path('product/prediction_history/', views.get_product_prediction_history, name='getProductPredictionHistory'),
]

