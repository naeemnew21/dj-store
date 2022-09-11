from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import MyUser, image_upload, OverwriteStorage
from django.utils import timezone
from django.core.exceptions import ValidationError





def validate_dimension(image):
    if image.width/image.height !=  1:
        raise ValidationError(
            [f'Size should be at least {1} / {1} percent.']
            )



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
    img = models.ImageField(upload_to=image_upload, 
                            default = 'product/product.png',
                            validators=[validate_dimension],
                            storage = OverwriteStorage() 
                            )

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
    created_by   = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(default=timezone.now)
    category     = models.CharField(max_length=50)
    brand        = models.CharField(max_length=50)
    name         = models.CharField(max_length=100)
    suitable     = models.CharField(choices=SEX, max_length= 5, blank=False, null=False)
    
    product_info = models.ManyToManyField(ProductInfo, blank=True)
    
    main_image   = models.ImageField(upload_to=image_upload,
                                     default = 'product/product.png',
                                     validators=[validate_dimension],
                                     storage = OverwriteStorage() 
                                     )
    image        = models.ManyToManyField(ProductImage, blank=True)
    description  = models.CharField(max_length=255, default="", blank=True, null=True)
    details      = models.TextField(blank=True, null=True) 
    
    slug         = models.SlugField(max_length = 255, null = False, blank = False)
    
    '''updated_info = ManyToMany-->
            updated_by
            updated_at
            info_changed
    '''
    
    '''number of selled products at all time'''
    selled     = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    
    def get_quantity(self, color = None, size = None):
        if color and size:
            qs = self.product_info.all().filter(color=color, size=size)
        elif color and not(size):
            qs = self.product_info.all().filter(color=color)
        elif not(color) and size:
            qs = self.product_info.all().filter(size=size)
        else:
            qs = self.product_info.all()
        quant = 0
        for record in qs:
            quant += record.quantity
        return quant
    
    
    def get_price(self, color, size):
        qs = self.product_info.all().filter(color=color, size=size)
        if qs.exists():
            return qs[0].price
        return None
    
    @property
    def get_colors(self):
        colors = set()
        for record in self.product_info.all():
            colors.add(record.color)
        return colors
    
    @property
    def get_sizes(self):
        sizes = set()
        for record in self.product_info.all():
            sizes.add(record.size)
        return sizes
    
    @property
    def get_rate(self):
        qs = self.comment__set.objects.all()
        if not(qs.exists()):
            return 0
        rate = 0
        for i in qs:
            rate += i.rate
        total_rate = rate / len(qs)
        return round(total_rate, 1)
    





class Comment(models.Model):
    user    = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length= 255, blank=True, null=True)
    rate    = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators = [MinValueValidator(0.0),MaxValueValidator(5.0)])
    
    def __str__(self):
        return str(self.id)
