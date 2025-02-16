#!/usr/bin/python3
"""User related models."""
import os
from django.db import models
from django.core.files.storage import default_storage
from django.core.files import File
from django.contrib.auth.models import AbstractUser, BaseUserManager


def user_image_upload_to(instance, filename):
    """
    Generate file path for user profile pictures.

    Args:
        instance: The instance of the model.
        filename: The original filename of the uploaded file.

    Returns:
        str: The file path where the image will be stored.
    """
    ext = filename.split('.')[-1]  # Get the file extension
    return os.path.join(f"profile_pictures/{instance.username}/profile.{ext}")


class CustomUserManager(BaseUserManager):
    """Custom user manager to handle email as username."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a new user with the given email and password.

        Args:
            email (str): The email address for the new user. This is required.
            password (str, optional): The password for the new user. If not
                provided, the user will have no password.
            **extra_fields: Additional fields to be set on the new user model.

        Raises:
            ValueError: If the email field is not set.

        Returns:
            CustomUser: The newly created user instance.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a new superuser with the given email and password.

        Args:
            email (str): The email address for the new superuser.
            This is required.
            password (str, optional): The password for the new superuser.
            If not provided, the superuser will have no password.
            **extra_fields: Additional fields to be set
            on the new superuser model.

        Raises:
            ValueError: If is_staff or is_superuser is set to False.

        Returns:
            CustomUser: The newly created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Retrieve a user by their natural key.

        Args:
            username (str): The username or email of the user.

        Returns:
            CustomUser: The user instance.
        """
        return self.get(
            models.Q(**{self.model.USERNAME_FIELD: username}) |
            models.Q(**{self.model.EMAIL_FIELD: username})
        )


class CustomUser(AbstractUser):
    """User profile model."""

    email = models.EmailField(unique=True, null=False, blank=False)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to=user_image_upload_to, default='default_user_image.png')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """Return a string representation of the user."""
        return "{} | id:{}".format(self.username, self.id)

    def save(self, *args, **kwargs):
        """
        Save the user instance and handle profile image.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        is_new = self.pk is None

        # First save to get the ID
        super().save(*args, **kwargs)

        # Handle the default image for new users
        if is_new and (
            not self.image or self.image.name == 'default_user_image.png'
        ):
            default_path = os.path.join('default_user_image.png')

            if default_storage.exists(default_path):
                user_specific_path = user_image_upload_to(
                    self, 'default_user_image.png')

                if not default_storage.exists(user_specific_path):
                    with default_storage.open(
                            default_path, 'rb') as default_file:
                        default_storage.save(
                            user_specific_path, File(default_file))

                    self.image = user_specific_path
                    super().save(update_fields=['image'])

        elif self.image and self.image.name != 'default_user_image.png':
            new_path = user_image_upload_to(self, self.image.name)
            if self.image.name != new_path:
                self.image.name = new_path
                super().save(update_fields=['image'])

    class Meta:
        """Meta options for the CustomUser model."""

        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
