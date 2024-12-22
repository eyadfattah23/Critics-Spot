#!/usr/bin/python3
"""admin Shelves handler"""
from django.contrib import admin
from .models import Shelf, ShelfBook
# Register your models here.

admin.site.register(Shelf)
admin.site.register(ShelfBook)
