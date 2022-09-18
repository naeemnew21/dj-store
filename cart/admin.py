from django.contrib import admin
from .models import NonUserOrder, Order

admin.site.register(Order)
admin.site.register(NonUserOrder)