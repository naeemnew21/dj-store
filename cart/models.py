from turtle import color
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from user.models import MyUser
from product.models import Product




class Order(models.Model):
    '''three comming fields are must to create order'''
    user      = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1, validators = [MinValueValidator(1)])
    # color     = models.CharField(max_length= 50, blank=False, null=False)
    # size      = models.CharField(max_length= 50, blank=False, null=False)
     
    confirmed     = models.BooleanField(default = False) # check if payment process done or not
    confirmed_at  = models.DateTimeField(blank=True, null=True)
    created_at    = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return str(self.id)
    
    @property
    def get_price(self):
        return self.product.price * self.quantity
    
         
    def save(self, *args, **kwargs):
        if self.confirmed and not(self.confirmed_at):
            self.confirmed_at = timezone.now()
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

