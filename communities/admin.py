#!/usr/bin/python3
"""admin Groups handler"""
from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_added', 'owner']


admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
