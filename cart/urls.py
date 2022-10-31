from django.urls import path
from . import api
from . import views

app_name = 'cart'


urlpatterns = [
    
    path('', views.cart_items, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('contact', views.contact, name = 'contact'),

    path('cart-api', api.CartApi.as_view(), name = 'cart_api'),
    path('del-order/<int:pk>', api.OrderDeleteApi.as_view(), name = 'del-order'),
    
]

