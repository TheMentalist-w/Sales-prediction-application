from django.urls import path
from .. import views


data_fetching_urlpatterns = [
    # fetching data from PitbullDB
    path('fetch/products/', views.fetch_products, name='fetchProducts'),
    path('fetch/groups/', views.fetch_groups, name='fetchGroups'),
    path('fetch/features/dict/', views.fetch_features_dict, name='fetchFeaturesDict'),
    path('fetch/features/dependencies/', views.fetch_product_features_dependencies, name='fetchProductFeaturesDependencies'),
    path('fetch/all/', views.fetch_all_data, name='fetchAllData'),
]
