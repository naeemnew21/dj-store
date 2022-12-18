from tabnanny import verbose
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.images import get_image_dimensions
from user.models import MyUser, image_upload, OverwriteStorage
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _





def validate_dimension(image):
    width, height = get_image_dimensions(image)
    if width != 500 or height !=  500:
        raise ValidationError(
            [f'Size should be  500*500 pixels.']
            )


CAT = [
    ('Shirts','Shirts'),
    ('Jeans','Jeans'),
    ('Swimwear','Swimwear'),
    ('Sleepwear','Sleepwear'),
    ('Sportswear','Sportswear'),
    ('Jumpsuits','Jumpsuits'),
    ('Blazers','Blazers'),
    ('Jackets','Jackets'),
    ('Shoes','Shoes')
    ]

COLOR =[
    ('Black','Black'),
    ('White','White'),
    ('Red','Red'),
    ('Blue','Blue'),
    ('Green','Green'),
    ('Yellow','Yellow'),
    ('Orange','Orange'),
    ('Brown','Brown'),
    ('Pink','Pink'),
    ('Rose','Rose')
    ]


SIZE =[
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL')
    ]


SEX =[
    ('All-Gender','All-Gender'),
    ('Male','Male'),
    ('Female','Female'),
    ('Baby','Baby')
    ]



    
class ProductImage(models.Model):
    img = models.ImageField(upload_to=image_upload, 
                            default = 'product/product.png',
                            validators=[validate_dimension],
                            storage = OverwriteStorage() , 
                            verbose_name=_('image')
                            )

    def __str__(self):
        return self.img.name.split('/')[1]

    class Meta:
        verbose_name= _("product image")
        verbose_name_plural = _('product images')


class SizeModel(models.Model):
    size  = models.CharField(max_length=20)
    def __str__(self):
        return self.size


class ColorModel(models.Model):
    color  = models.CharField(max_length=20)
    def __str__(self):
        return self.color



class Product(models.Model):
    created_by   = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_('created by'))
    created_at   = models.DateTimeField(default=timezone.now, verbose_name=_('created at'))
    category     = models.CharField(choices=CAT, max_length=50, verbose_name=_('category'))
    brand        = models.CharField(max_length=50, verbose_name=_('brand'))
    name         = models.CharField(max_length=100, verbose_name=_('name'))
    suitable     = models.CharField(choices=SEX, max_length= 20, blank=False, null=False, verbose_name=_('suitable'))
    
    colors       = models.ManyToManyField(ColorModel, blank=True, verbose_name=_('colors'))
    sizes        = models.ManyToManyField(SizeModel, blank=True, verbose_name=_('sizes'))
    
    quantity     = models.PositiveIntegerField(default=0, verbose_name=_('quantity'))
    price        = models.DecimalField(max_digits=7, decimal_places=2, validators = [MinValueValidator(0.0)], verbose_name=_('price'))
    price_dis    = models.DecimalField(max_digits=7, decimal_places=2, validators = [MinValueValidator(0.0)], verbose_name=_('price before discount'))
    
    main_image   = models.ImageField(upload_to=image_upload,
                                     default = 'product/product.png',
                                     validators=[validate_dimension],
                                     storage = OverwriteStorage(), 
                                     verbose_name=_('main image')
                                     )
    image        = models.ManyToManyField(ProductImage, blank=True, verbose_name=_('image'))
    description  = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name=_('description'))
    details      = models.TextField(blank=True, null=True, verbose_name=_('details')) 
    
    slug         = models.SlugField(max_length = 255, null = False, blank = False, unique=True, verbose_name=_('slug'))
    
    '''number of selled products at all time'''
    selled     = models.PositiveIntegerField(default=0, verbose_name=_('selled'))
    approved   = models.BooleanField(default = False, verbose_name=_('approved'))
    

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


    def __str__(self):
        return self.name
    

    @property
    def get_colors(self):
        colors = set()
        for record in self.colors.all():
            colors.add(record.color)
        return colors
    
    @property
    def get_colors_ids(self):
        colors = []
        for record in self.colors.all():
            colors.append(record.id)
        return colors

    @property
    def get_sizes(self):
        sizes = set()
        for record in self.sizes.all():
            sizes.add(record.size)
        return sizes

    @property
    def get_sizes_ids(self):
        sizes = []
        for record in self.sizes.all():
            sizes.append(record.id)
        return sizes

    @property
    def get_rate(self):
        qs = Comment.objects.filter(product = self)
        if not(qs.exists()):
            return 0
        rate = 0
        for i in qs:
            rate += i.rate
        total_rate = rate / len(qs)
        return round(total_rate, 1)
    





class Comment(models.Model):
    user       = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_('user'))
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    comment    = models.CharField(max_length= 255, blank=True, null=True, verbose_name=_('comment'))
    rate       = models.DecimalField(max_digits=2, decimal_places=1, default=0, 
                                     validators = [MinValueValidator(0.0),MaxValueValidator(5.0)],
                                     verbose_name=_('rate'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('created at'))

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')



class Statics(models.Model):
    all_products = models.PositiveIntegerField(default=0)

    price100 = models.PositiveIntegerField(default=0)
    price200 = models.PositiveIntegerField(default=0)
    price300 = models.PositiveIntegerField(default=0)
    price400 = models.PositiveIntegerField(default=0)
    price500 = models.PositiveIntegerField(default=0)

    black = models.PositiveIntegerField(default=0)
    white = models.PositiveIntegerField(default=0)
    red   = models.PositiveIntegerField(default=0)
    blue  = models.PositiveIntegerField(default=0)
    green = models.PositiveIntegerField(default=0)

    xs  = models.PositiveIntegerField(default=0)
    s   = models.PositiveIntegerField(default=0)
    m   = models.PositiveIntegerField(default=0)
    l   = models.PositiveIntegerField(default=0)
    xl  = models.PositiveIntegerField(default=0)
    xxl = models.PositiveIntegerField(default=0)

    male   = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    baby   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Statics')
        verbose_name_plural = _('Statics')
