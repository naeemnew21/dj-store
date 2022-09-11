from rest_framework.generics import GenericAPIView, DestroyAPIView
from django.db.models.query import EmptyQuerySet
from rest_framework.response import Response
from rest_framework import status
from .models import Order, NonUserOrder
from product.models import Product
from .serializers import OrderSerializer, OrderDelSerializer






class CartApi(GenericAPIView):
    serializer_class   = OrderSerializer

    
    def get_queryset(self):
        user  = self.request.user
        user_cart_id = self.request.COOKIES.get('user_cart_id')
        if user.is_authenticated:
            return Order.objects.filter(user = user, confirmed = False)
        if user_cart_id == None:
            return EmptyQuerySet
        return NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    
 
        
    def post(self, request, *args, **kwargs):
        user = request.user
        user_cart_id = self.request.COOKIES.get('user_cart_id')
        try:
            product  = Product.objects.get(id = request.data['product'] )
            quantity = int(request.data['quantity'])
            action   = request.data['action'] # add or remove
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(user=user, product=product, confirmed = False)
            if action == 'add':
                if order.quantity + quantity > order.product.quantity:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                order.quantity += quantity
            elif action=='remove':
                order.quantity -= quantity
            order.save()
            if order.quantity <= 0 :
                order.delete()   
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        
        if user_cart_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        order, created = NonUserOrder.objects.get_or_create(user_cart_id=user_cart_id, product=product)
        if action == 'add':
            if order.quantity + quantity > order.product.quantity:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            order.quantity += quantity
        elif action=='remove':
            order.quantity -= quantity
        order.save()
        if order.quantity <= 0 :
            order.delete()   
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_201_CREATED)
    
    
    


class OrderDeleteApi(DestroyAPIView):
    serializer_class   = OrderSerializer
    
    def get_queryset(self):
        user  = self.request.user
        user_cart_id = self.request.COOKIES.get('user_cart_id')
        if user.is_authenticated:
            return Order.objects.filter(user = user, confirmed = False)
        if user_cart_id == None:
            return EmptyQuerySet
        return NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    
 