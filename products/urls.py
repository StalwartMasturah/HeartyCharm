from django.urls import path
from .views import *

urlpatterns = [
    path('', shop_home, name='shop'),
    path('category/<slug:slug>/', category_products, name='category_products'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('custom-order/', custom_order_form, name='custom_order_form'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/<str:action>/', update_cart, name='update_cart'), 
    path('checkout/', checkout, name='checkout'), 
    path('cart_view/', cart_view, name='cart_view'),
    path('pay/<int:order_id>/', start_payment, name='start_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
    path('payment-success/', payment_success, name='payment_success'),


]