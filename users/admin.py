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

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image', 'email', 'first_name', 'last_name')}),
    )
    search_fields = ['username__startswith',
                     'first_name__startswith', 'last_name__startswith']


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__email']
    ordering = ['created_at']
    autocomplete_fields = ['book', 'user']


# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Favorite)
