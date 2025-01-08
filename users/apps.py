#!/usr/bin/python3
"""App configuration for the users app."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the users app."""

    name = 'users'

    def ready(self):
        """Import signals when the app is ready."""
        import users.signals
