from django.shortcuts import render
from project.settings import CART_SESSION_ID_KEY
from django.db.models.query import EmptyQuerySet
from .models import Order, NonUserOrder



def cart_items(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        total = sum([order.get_price for order in orders])
        context = {'orders':orders, 'total': total}
        return render(request, 'cart.html' , context)
    
    if user_cart_id == None:
        context = {'orders':EmptyQuerySet, 'total':0}
        return render(request, 'cart.html' , context)
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    total = sum([order.get_price for order in orders])
    context = {'orders':orders, 'total': total}
    return render(request, 'cart.html' , context)





def checkout(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        total = sum([order.get_price for order in orders])
        context = {'orders':orders, 'total': total}
        return render(request, 'checkout.html' , context)
    
    if user_cart_id == None:
        context = {'orders':EmptyQuerySet, 'total':0}
        return render(request, 'checkout.html' , context)
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    total = sum([order.get_price for order in orders])
    context = {'orders':orders, 'total': total}
    return render(request, 'checkout.html' , context)






def contact(request):
    return render(request, 'contact.html' )



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