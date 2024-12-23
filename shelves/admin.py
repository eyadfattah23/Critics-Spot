#!/usr/bin/python3
"""admin Shelves handler"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Shelf, ShelfBook
# Register your models here.


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'number_of_books']

    def number_of_books(self, shelf):
        """Count the number of books in a shelf."""
        url = (reverse('admin:shelves_shelfbook_changelist')
               + '?'
               + urlencode({'shelf__id': str(shelf.id)}))
        return format_html('<a href="{}">{}</a>', url, shelf.shelfbook_set.count())
        return shelf.shelfbook_set.count()
    number_of_books.short_description = 'Number of Books'


admin.site.register(ShelfBook)
