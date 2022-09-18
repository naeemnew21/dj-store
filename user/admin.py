from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from django.contrib.auth.models import Group

admin.site.site_header = 'E-Commerce'


class CustomUserAdmin(UserAdmin):
    model = MyUser
    list_display = [ 'email', 'is_verified', 'seller', 'is_staff', 'is_superuser', 'auth_provider']
    list_display_links = ['email']
    
    search_fields   = ('email', 'phone',)
    list_filter     = ('is_superuser', 'date_joined')
    readonly_fields =('date_joined', 'last_login', 'username', 'auth_provider')
     
    fieldsets = (
        (None, 
            {'fields': ('first_name', 'last_name','username', 'auth_provider', 'email', 'password', 'phone', 'avatar', 'avatar_url', 'address')}
        ),
        ('Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'seller')}
         ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = ( (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'auth_provider', 'email', 'password1', 'password2', 'phone', 'username', 'is_superuser', 'is_verified','address', 'avatar')}
        ),
                     )
    





admin.site.register(MyUser, CustomUserAdmin)
admin.site.unregister(Group)