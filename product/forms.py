from django import forms
from .models import Product



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 
                  'brand',
                  'name',
                  'suitable',
                  'colors',
                  'sizes',
                  'quantity', 
                  'price',
                  'price_dis',
                  'main_image',
                  'details',
                   )




