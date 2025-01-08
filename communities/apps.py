"""App configuration for the communities app."""
from django.apps import AppConfig


class CommunitiesConfig(AppConfig):
    """Configuration for the communities app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communities'

    def ready(self):
        """Perform initialization tasks for the communities app."""
        import communities.signals
