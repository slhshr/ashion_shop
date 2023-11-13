from django.urls import path
from .views import *

app_name = 'product'
urlpatterns = [
    path('search/', search, name='search'),
    path('customer_profile/', customer_profile, name='customer_profile'),
    path('details/<str:pk>', product_details, name='details'),
    path('category/<int:id>', category, name='category'),
    path('delete/<str:pk>', delete_product, name='delete'),
    path('new/', new_product, name='new_product'),
    path('update/<str:pk>', update_product, name='update_product'),
    path('shipping_address/', shipping_address, name='shipping_address'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/', update_cart, name='update_cart'),
    path('order_status/', order_status, name='order_status'),
    path('order_factor/', order_factor, name='order_factor')
]