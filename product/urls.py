
from django.urls import path
from . import views 
from . import api

app_name = 'product'


urlpatterns = [
    path('', views.index , name = 'index'),
    path('add-product', api.ProductCrreateApi.as_view(), name = 'add-product'),
    path('del-product/<int:pk>', api.ProductDeleteApi.as_view(), name = 'del-product'),
]

