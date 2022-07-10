from django.urls import path
from .views import *

urlpatterns = [
    path('',MainView.as_view(),name='main'),
    path('products/',ProductListView.as_view(), name='products'),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    path('new-collection/',NewCollectionListView.as_view(),name='new_collection'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add_quantity/<int:product_id>/',add_quantity_view,name='add_quantity'),
    path('remove_quantity/<int:product_id>/',remove_quantity_view,name='remove_quantity'),
    path('add_cart/<int:product_id>/',AddCartView.as_view(),name='add_cart'),
    path('remove_cart/<int:product_id>/',remove_from_cart_view,name='remove_cart'),
    path('recommended/',RecommendedProductView.as_view(),name='recommended'),
]