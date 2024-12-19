#!/usr/bin/python3
"""admin User handler"""

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Customizing the UserAdmin to include additional fields


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add the 'profile_image' field to the fieldsets (used for editing)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )

    # Add the 'profile_image' field to add/edit user form views
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )


# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
