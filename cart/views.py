from django.shortcuts import render
from project.settings import CART_SESSION_ID_KEY
from django.db.models.query import EmptyQuerySet
from .models import Order, NonUserOrder



def cart_items(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        context = {'orders':orders}
        render(request, 'cart.html' , context)
    
    if user_cart_id == None:
        context = {'orders':EmptyQuerySet}
        render(request, 'cart.html' , context)
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    context = {'orders':orders}
    render(request, 'cart.html' , context)



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