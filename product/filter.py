import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    details     = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name',
                 'color1', 'color2', 'color3', 'color4', 'color5',
                 'description',
                 'details',
                 ]