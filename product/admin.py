from django.contrib import admin
from .models import ProductImage, Product, Comment




class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [ 'name', 'category', 'brand', 'suitable']
    readonly_fields=('created_by', 'created_at', 'slug', 'selled', 'id')
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    #readonly_fields=('created_by', 'created_at', 'slug', 'selled')
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
        

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Comment, CommentAdmin)