
from django.urls import path
from . import views 
from . import api

app_name = 'product'

urlpatterns = [
    path('', views.index , name = 'index'),
    path('shop', views.CategoryView.as_view(), name = 'shop'),
    path('detail/<str:slug>', views.ProductDetailView.as_view(), name = 'detail'),

    #path('dashboard', views.dashboard, name = 'dashboard'),
    path('dashboard', views.ProductCreateView.as_view(), name = 'dashboard'),
    path('delete-product/<str:slug>', views.ProductDeleteView.as_view(), name = 'delete-product'),
    path('update-product/<str:slug>', views.ProductUpdateView.as_view(), name = 'update-product'),

    # path('add-product', api.ProductCrreateApi.as_view(), name = 'add-product'),
    # path('del-product/<int:pk>', api.ProductDeleteApi.as_view(), name = 'del-product'),
]

