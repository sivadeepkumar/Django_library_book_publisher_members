from django.contrib import admin
from .models import *
from products.models import *
# Register your models here.
admin.site.register(Publisher)
admin.site.register(Book)

admin.site.register(Borrowing)
# admin.site.register(Product)  
# admin.site.register(UserDetails)


# library/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('email', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)
