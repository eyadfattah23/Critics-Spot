#!/usr/bin/python3
"""admin Groups handler"""
from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'death_date',
                    'number_of_books']

    def number_of_books(self, obj):
        """Count the number of books written by an author."""
        return obj.book_set.count()
    number_of_books.short_description = 'Number of books'


admin.site.register(Genre)
admin.site.register(Book)
