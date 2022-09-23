from django import forms
from .models import Product



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 
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
                   )



