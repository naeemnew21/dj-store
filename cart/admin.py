from django.contrib import admin
from .models import NonUserOrder, Order, CheckOut



class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id',  'user', 'product', 'quantity', 'confirmed', 'track']
    list_editable = ('track', )
    readonly_fields=('confirmed_at', 'created_at')

    search_fields   = ('id', 'user', 'confirmed')
    list_filter     = ('confirmed', 'track')
    
    

class CheckOutAdmin(admin.ModelAdmin):
    model = Order
    list_display = [ 'user', 'get_orders', 'phone', 'active']
    list_editable = ('active', )
    readonly_fields=('created_at',)

    search_fields   = ('id', 'user', 'phone')
    list_filter     = ('active', 'created_at')

    def get_orders(self, obj):
        return ",".join([str(i) for i in obj.orders.all()])
    
    


admin.site.register(Order, OrderAdmin)
admin.site.register(NonUserOrder)
admin.site.register(CheckOut, CheckOutAdmin)