from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    USER = "USER", "Пользователь"
    ADMIN = "ADMIN", "Администратор"

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    REQUIRED_FIELDS = ["email"]

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN or self.is_superuser
    
    def save(self, *args, **kwargs):
        if self.role == Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)
