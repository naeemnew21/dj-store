from django.urls import path
from . import views 

app_name = 'user'


urlpatterns = [
    path('cart', views.cart , name = 'cart'),
    path('checkout', views.checkout , name = 'checkout'),
    path('contact', views.contact , name = 'contact'),
    path('detail', views.detail , name = 'detail'),
    path('index', views.index , name = 'index'),
    path('login', views.logintest , name = 'login'),
    path('register', views.register , name = 'register'),
    path('shop', views.shop , name = 'shop'),

    path('login', views.login_view , name = 'login'),
    path('logout', views.logout_view , name = 'logout'),
    path('sign-up', views.Registeration.as_view() , name = 'sign-up'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    

]

