from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="user_photos/",
        null=True,
        blank=True,
        verbose_name="Foto de Perfil",
    )

    birth_date = models.DateField(
        null=True, blank=True, verbose_name="Data de Aniversário"
    )

    objects: UserManager = UserManager()

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["first_name", "last_name"]
