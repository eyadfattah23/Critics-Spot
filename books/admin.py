#!/usr/bin/python3
"""admin Groups handler"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import *
# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'death_date',
                    'number_of_books']

    def number_of_books(self, author):
        """Count the number of books written by an author.
            redirect to books only written by the author"""
        url = (reverse('admin:books_book_changelist')
               + '?'
               + urlencode({'author__id': str(author.id)}))
        return format_html('<a href="{}">{}</a>', url, author.book_set.count())

        return author.book_set.count()
    number_of_books.short_description = 'Number of books'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_books']

    def number_of_books(self, genre):
        """Count the number of books in a genre.
            redirect to books only in the genre"""
        url = (reverse('admin:books_book_changelist')
               + '?'
               + urlencode({'genre__id': str(genre.id)}))
        return format_html('<a href="{}">{}</a>', url, genre.books.count())

        return genre.book_set.count()
    number_of_books.short_description = 'Number of books'


admin.site.register(Book)
