from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import MyUser, image_upload, OverwriteStorage
from django.utils import timezone
from django.core.exceptions import ValidationError





def validate_dimension(image):
    if image.width != 500 or image.height !=  500:
        raise ValidationError(
            [f'Size should be  500*500 pixels.']
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




class Product(models.Model):
    created_by   = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(default=timezone.now)
    category     = models.CharField(max_length=50)
    brand        = models.CharField(max_length=50)
    name         = models.CharField(max_length=100)
    suitable     = models.CharField(choices=SEX, max_length= 5, blank=False, null=False)
    
    color1       = models.CharField(max_length= 50, blank=False, null=False)
    color2       = models.CharField(max_length= 50, blank=True, null=True)
    color3       = models.CharField(max_length= 50, blank=True, null=True)
    color4       = models.CharField(max_length= 50, blank=True, null=True)
    color5       = models.CharField(max_length= 50, blank=True, null=True)
    size1        = models.CharField(max_length= 50, blank=False, null=False)
    size2        = models.CharField(max_length= 50, blank=True, null=True)
    size3        = models.CharField(max_length= 50, blank=True, null=True)
    size4        = models.CharField(max_length= 50, blank=True, null=True)
    size5        = models.CharField(max_length= 50, blank=True, null=True)
    size6        = models.CharField(max_length= 50, blank=True, null=True)
    
    quantity     = models.PositiveIntegerField(default=0)
    price        = models.DecimalField(max_digits=7, decimal_places=2, validators = [MinValueValidator(0.0)])
    
    main_image   = models.ImageField(upload_to=image_upload,
                                     default = 'product/product.png',
                                     validators=[validate_dimension],
                                     storage = OverwriteStorage() 
                                     )
    image        = models.ManyToManyField(ProductImage, blank=True)
    description  = models.CharField(max_length=255, default="", blank=True, null=True)
    details      = models.TextField(blank=True, null=True) 
    
    slug         = models.SlugField(max_length = 255, null = False, blank = False)
    
    '''number of selled products at all time'''
    selled     = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
 

    @property
    def get_colors(self):
        colors = set()
        for color in [self.color1, self.color2, self.color3, self.color4,self.color5,]:
            if color:
             colors.add(color)
        return colors
    
    @property
    def get_sizes(self):
        sizes = set()
        for size in [self.size1, self.size2, self.size3, self.size4, self.size5, self.size6]:
            if size:
               sizes.add(size)
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
