from django.contrib import admin
from .models import ProductImage, Product, Comment




class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [ 'name', 'category', 'brand', 'suitable', 'approved', 'quantity', 'price', 'selled']
    list_editable = ('approved', )
    readonly_fields=('created_by', 'created_at', 'slug', 'selled', 'id')

    search_fields   = ('name', 'description', 'details',
                         'color1', 'color2', 'color3', 'color4', 'color5',
                         'size1', 'size2', 'size3', 'size4', 'size5', 'size6',
                         )
    list_filter     = ('approved', 'category', 'suitable')
    
    def save_model(self, request, obj, form, change):
        try:
            if obj.created_by == None:
                obj.created_by = request.user
        except:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
        

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Comment, CommentAdmin)