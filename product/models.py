from asyncio.windows_events import NULL
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from user.models import MyUser, image_upload, OverwriteStorage
from django.utils import timezone




COLOR =[
    ('red','red'),
    ('blue','blue'),
    ('black','black')
    ]


SIZE =[
    ('s','s'),
    ('m','m'),
    ('l','l')
    ]


SEX =[
    ('men','men'),
    ('women','women'),
    ('all','all')
    ]



    
class ProductImage(models.Model):
    img = models.ImageField(upload_to=image_upload, default = 'product/product.png', storage = OverwriteStorage() )

    def __str__(self):
        return self.img.name.split('/')[1]



class ProductInfo(models.Model):
    color    = models.CharField(choices=COLOR, max_length= 10, blank=False, null=False)
    size     = models.CharField(choices=SIZE, max_length= 10, blank=False, null=False)
    price    = models.DecimalField(max_digits=7, decimal_places=2, validators = [MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return '-'.join((str(self.id), self.color, self.size))




class Product(models.Model):
    user         = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category     = models.CharField(max_length=50)
    brand        = models.CharField(max_length=50)
    name         = models.CharField(max_length=100)
    suitable     = models.CharField(choices=SEX, max_length= 5, blank=False, null=False)
    
    product_info = models.ManyToManyField(ProductInfo, blank=True)
    
    main_image   = models.ImageField(upload_to=image_upload, default = 'product/product.png', storage = OverwriteStorage() )
    image        = models.ManyToManyField(ProductImage, blank=True)
    description  = models.CharField(max_length=250, default="", blank=True, null=True)
    details      = models.TextField(blank=True, null=True) 
    
    slug         = models.SlugField(max_length = 250, null = True, blank = True)

    
    '''number of selled products at all time'''
    selled     = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name





class Comment(models.Model):
    user         = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    #rate
    def __str__(self):
        return '-'.join((str(self.id), self.color, self.size))
