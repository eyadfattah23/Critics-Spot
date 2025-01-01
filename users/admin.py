#!/usr/bin/python3
"""admin User handler"""

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Favorite, BookReview

# Customizing the UserAdmin to include additional fields


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff']

    # For adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'image', 'first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
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


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'book__title']
    search_fields = ['book__title', 'user__email', 'user__username']
    ordering = ['created_at']
    autocomplete_fields = ['book', 'user']

    list_select_related = ['book', 'user']


# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Favorite)
