#!/usr/bin/python3
"""Admin Groups handler."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import *
# Register your models here.


class BookBookReviewInline(admin.TabularInline):
    """Inline admin class for book reviews."""

    model = BookReview
    autocomplete_fields = ['user']


class AuthorBookInline(admin.TabularInline):
    """Inline admin class for books by an author."""

    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin class for managing authors."""

    list_display = ['id', 'name', 'birth_date', 'death_date',
                    'number_of_books']
    search_fields = ['name']
    inlines = [AuthorBookInline]
    prepopulated_fields = {'slug': ('name',)}

    def number_of_books(self, author):
        """Count the number of books written by an author.

        Redirect to books only written by the author.
        """
        url = (reverse('admin:books_book_changelist')
               + '?'
               + urlencode({'author__id': str(author.id)}))
        return format_html('<a href="{}">{}</a>', url, author.books.count())

        return author.book_set.count()
    number_of_books.short_description = 'Number of books'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin class for managing genres."""

    list_display = ['id', 'name', 'number_of_books']

    def number_of_books(self, genre):
        """Count the number of books in a genre.

        Redirect to books only in the genre.
        """
        url = (reverse('admin:books_book_changelist')
               + '?'
               + urlencode({'genres__id': str(genre.id)}))
        return format_html('<a href="{}">{}</a>', url, genre.books.count())

        return genre.book_set.count()
    number_of_books.short_description = 'Number of books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin class for managing books."""

    list_display = ['id', 'title', 'pages', 'author',
                    'avg_rating', 'number_of_reviews']
    search_fields = ['title', 'pages', 'author__name__istartswith']

    list_filter = ['genres']
    inlines = [BookBookReviewInline]
    # autocomplete_fields = ['author', 'title']
    list_select_related = ['author']
    prepopulated_fields = {'slug': ('title',)}

    def number_of_reviews(self, book):
        """Count the number of reviews of a book.

        Redirect to reviews of the book.
        """
        url = (reverse('admin:books_bookreview_changelist')
               + '?'
               + urlencode({'book__id': str(book.id)}))
        return format_html(
            '<a href="{}">{}</a>',
            url,
            book.bookreview_set.count())

        return book.bookreview_set.count()


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """Admin class for managing book reviews."""

    list_display = ['id', 'user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'book__title']
    search_fields = ['book__title', 'user__email', 'user__username']
    ordering = ['created_at']
    autocomplete_fields = ['book', 'user']

    list_select_related = ['book', 'user']
