from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Product




class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Product
        fields = ['created_by',
                  'category', 
                  'brand',
                  'name',
                  'suitable',
                  'color1','color2','color3','color4','color5',
                  'size1','size2','size3','size4','size5','size6',
                  'quantity', 
                  'price',
                  'price_dis',
                  'main_image',
                  'details',
                   ]
        

