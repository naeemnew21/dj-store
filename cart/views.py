from django.shortcuts import render
from project.settings import CART_SESSION_ID_KEY
from .models import Order, NonUserOrder





def cart_context(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        total = sum([item.quantity for item in orders])
        return {'my_cart':total}
    
    if user_cart_id == None:
        return {'my_cart':0}
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    total = sum([item.quantity for item in orders])
    return {'my_cart':total}