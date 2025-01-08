#!/usr/bin/python3
"""Admin Shelves handler."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Shelf, ShelfBook
# Register your models here.


class ShelfBookInline(admin.TabularInline):
    """Inline admin interface for ShelfBook model."""

    autocomplete_fields = ['book', 'shelf']
    model = ShelfBook


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    """Admin interface for Shelf model."""

    list_display = ['id', 'name', 'user',
                    'number_of_books', 'is_default', 'image']
    list_select_related = ['user']
    search_fields = ['name', 'user__username']
    inlines = [ShelfBookInline]
    autocomplete_fields = ['user']

    def number_of_books(self, shelf):
        """Count the number of books in a shelf."""
        url = (reverse('admin:shelves_shelfbook_changelist')
               + '?'
               + urlencode({'shelf__id': str(shelf.id)}))
        return format_html(
            '<a href="{}">{}</a>',
            url,
            shelf.shelfbook_set.count())
        return shelf.shelfbook_set.count()
    number_of_books.short_description = 'Number of Books'


@admin.register(ShelfBook)
class ShelfBookAdmin(admin.ModelAdmin):
    """Admin interface for ShelfBook model."""

    autocomplete_fields = ['shelf', 'book']
    list_select_related = ['shelf', 'book']
    list_display = ['id', 'book', 'shelf', 'current_page']
