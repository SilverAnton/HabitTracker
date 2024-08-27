from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(
        max_length=100, verbose_name="phone", null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to="users/", verbose_name="avatar", null=True, blank=True
    )
    country = models.CharField(
        max_length=150, verbose_name="country", null=True, blank=True
    )
    token = models.CharField(
        max_length=100, verbose_name="token", null=True, blank=True
    )
    is_active = models.BooleanField(
        default=True, verbose_name="is_active status", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = (
        CustomUserManager()
    )  # Использую кастомный менеджер(без него просит username в тесте)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
