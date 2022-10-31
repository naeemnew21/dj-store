from rest_framework import serializers
from .models import Order





class OrderSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=['add', 'remove'])
    class Meta:
        model = Order
        fields = ('product', 'quantity', 'action')


class OrderDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product',)