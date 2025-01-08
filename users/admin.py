#!/usr/bin/python3
"""admin User handler."""

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Customizing the UserAdmin to include additional fields


class CustomUserAdmin(UserAdmin):
    """Custom user admin with additional fields."""

    model = CustomUser
    list_display = ['id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff']

    # For adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'image', 'first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff',
                'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

    # For editing existing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name',
         'last_name', 'email', 'image', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    search_fields = ['username__startswith',
                     'first_name__startswith', 'last_name__startswith']
    list_per_page = 10


# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
