from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Create your models here.
class CustomUserManager(BaseUserManager):
    """Manager for custom user."""

    def create_user(self, email, password=None, **extra_field):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_field
        )

        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_field):
        """
        Creates and saves a User with the given email, password, and set is_staff and is_superuser to True.
        """
        user = self.create_user(email=email, password=password, **extra_field)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
