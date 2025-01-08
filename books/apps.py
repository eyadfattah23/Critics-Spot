#!/usr/bin/python3
"""App configuration for the books app."""

from django.apps import AppConfig


class BooksConfig(AppConfig):
    """Configuration for the books app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):
        """Run when the app is ready."""
        import books.signals  # Import signals here
