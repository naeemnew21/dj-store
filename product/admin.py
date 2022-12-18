from django.contrib import admin
from .models import ProductImage, Product, Comment, ColorModel, SizeModel, Statics
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _



class ProductAdmin(TranslationAdmin):
    model = Product
    list_display = ['name_en', 'category', 'brand', 'suitable', 'approved', 'quantity', 'price', 'selled']
    list_display_links = ['name_en']
    list_editable = ('approved', )
    readonly_fields=('created_by', 'created_at', 'slug', 'selled', 'id')

    search_fields   = ('name', 'description', 'details')
    list_filter     = ('approved', 'category', 'suitable')
    group_fieldsets = True  

    def save_model(self, request, obj, form, change):
        try:
            if obj.created_by == None:
                obj.created_by = request.user
        except:
            obj.created_by = request.user
        
        #update statics model
        static, created = Statics.objects.get_or_create(id = 0)
        static.all_products = Product.objects.all().count()
        static.price100 = Product.objects.filter(approved=True, price__range = [0,100]).count()
        static.price200 = Product.objects.filter(approved=True, price__range = [100,200]).count()
        static.price300 = Product.objects.filter(approved=True, price__range = [200,300]).count()
        static.price400 = Product.objects.filter(approved=True, price__range = [300,400]).count()
        static.price500 = Product.objects.filter(approved=True, price__range = [400,500]).count()
        static.black    = Product.objects.filter(approved=True, colors__color = 'Black').count()
        static.white    = Product.objects.filter(approved=True, colors__color = 'white').count()
        static.red      = Product.objects.filter(approved=True, colors__color = 'red').count()
        static.blue     = Product.objects.filter(approved=True, colors__color = 'blue').count()
        static.green    = Product.objects.filter(approved=True, colors__color = 'green').count()
        static.xs       = Product.objects.filter(approved=True, sizes__size = 'XS').count()
        static.s        = Product.objects.filter(approved=True, sizes__size = 'S').count()
        static.m        = Product.objects.filter(approved=True, sizes__size = 'M').count()
        static.l        = Product.objects.filter(approved=True, sizes__size = 'L').count()
        static.xl       = Product.objects.filter(approved=True, sizes__size = 'XL').count()
        static.xxl      = Product.objects.filter(approved=True, sizes__size = 'XXL').count()
        static.male     = Product.objects.filter(approved=True, suitable = "Male").count()
        static.female   = Product.objects.filter(approved=True, suitable = "Female").count()
        static.baby     = Product.objects.filter(approved=True, suitable = "Baby").count()
        static.save()
        super().save_model(request, obj, form, change)
    

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
    
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
admin.site.register(ColorModel)
admin.site.register(SizeModel)
admin.site.register(Comment, CommentAdmin)