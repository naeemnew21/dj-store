from django.shortcuts import render, redirect
from project.settings import CART_SESSION_ID_KEY, CHARGE_PRICE
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.decorators import login_required
from .models import Order, NonUserOrder
from .forms import CheckOutCreateForm



def cart_items(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        confirmed = Order.objects.filter(user = user, confirmed = True)
        total = sum([order.get_price for order in orders])
        context = {'confirmed':confirmed, 'orders':orders, 'total': total, 'totch':total+CHARGE_PRICE}
        return render(request, 'cart.html' , context)
    
    if user_cart_id == None:
        context = {'orders':EmptyQuerySet, 'total':0, 'totch':0}
        return render(request, 'cart.html' , context)
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    total = sum([order.get_price for order in orders])
    context = {'orders':orders, 'total': total, 'totch':total+CHARGE_PRICE}
    return render(request, 'cart.html' , context)





@login_required
def checkout(request):
    context = {}
    user = request.user

    if request.POST:
        
        orders = Order.objects.filter(user = user, confirmed = False)
        if not(orders.exists()):
            return redirect('cart:cart') 

        form = CheckOutCreateForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.user = user
            checkout.save()

            for i in orders:
                checkout.orders.add(i)
                i.confirmed = True
                i.save()
                # Edit selled quantity
                i.product.quantity -= i.quantity
                i.product.selled += i.quantity
                i.product.save()

            return redirect('cart:cart') 
        else:
            context['form'] = form
    else: # GET request
        form = CheckOutCreateForm()
        context['form'] = form

    orders = Order.objects.filter(user = user, confirmed = False)
    total = sum([order.get_price for order in orders])
    context.update({'orderscount':len(orders), 'orders':orders, 'total': total, 'totch':total+CHARGE_PRICE})
    return render(request, 'checkout.html' , context)
    






def contact(request):
    return render(request, 'contact.html' )



def cart_context(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        total = sum([item.quantity for item in orders])
        return {'my_cart':total, 'charge_price':CHARGE_PRICE}
    
    if user_cart_id == None:
        return {'my_cart':0, 'charge_price':0}
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    total = sum([item.quantity for item in orders])
    return {'my_cart':total, 'charge_price':CHARGE_PRICE}