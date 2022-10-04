from enum import unique
from turtle import color
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, RegexValidator
from user.models import MyUser
from product.models import Product




TRACK =[
    ('Not-Charged','Not-Charged'),
    ('On-way','On-way'),
    ('Delivered','Delivered')
    ]



class Order(models.Model):
    '''three comming fields are must to create order'''
    user      = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=0, validators = [MinValueValidator(0)])
     
    confirmed     = models.BooleanField(default = False) # check if payment process done or not
    confirmed_at  = models.DateTimeField(blank=True, null=True)
    created_at    = models.DateTimeField(default=timezone.now)
    
    track = models.CharField(default='Not-Charged', choices=TRACK, max_length= 20, blank=False, null=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_price(self):
        return self.product.price * self.quantity
    
         
    def save(self, *args, **kwargs):
        if self.confirmed and not(self.confirmed_at):
            self.confirmed_at = timezone.now()
            self.track = 'On-way'
        super().save(*args, **kwargs)
    
    
    
    
    
    
    
    
class NonUserOrder(models.Model):
    user_cart_id = models.CharField(max_length= 50, blank=True, null=True)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity     = models.PositiveIntegerField(default=0, validators = [MinValueValidator(0)])

    def __str__(self):
        return str(self.id)


    @property
    def get_price(self):
        return self.product.price * self.quantity






class CheckOut(models.Model):
    user   = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, blank = True)
    
    phone_regex   = RegexValidator(regex="[0][1][0125][0-9][ ]?\d{3}[ ]?\d{4}", message="Phone number must be entered in the format: '01xx xxx xxxx'. Up to 11 digits allowed.")
    phone         = models.CharField(validators=[phone_regex], max_length=11, blank=False, null=False) # validators should be a list
    
    country = models.CharField(max_length=50, blank=True, null=True)
    city    = models.CharField(max_length=50, blank=True, null=True)
    add1    = models.CharField(max_length=50, blank=True, null=True)
    add2    = models.CharField(max_length=50, blank=True, null=True)

    active  = models.BooleanField(default = True)
    created_at    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
