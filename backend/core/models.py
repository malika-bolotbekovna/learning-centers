from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    def __str__(self): return self.name

class Center(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    social_vk = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_telegram = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.name

class ProgramFormat(models.TextChoices):
    ONLINE = "ONLINE", "Онлайн"
    OFFLINE = "OFFLINE", "Оффлайн"
    MIXED = "MIXED", "Смешанный"

class Program(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="programs")
    topic = models.CharField(max_length=120, blank=True)
    format = models.CharField(max_length=10, choices=ProgramFormat.choices, default=ProgramFormat.OFFLINE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default="KGS")
    schedule = models.CharField(max_length=200, blank=True)
    age_min = models.PositiveIntegerField(null=True, blank=True)
    age_max = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.title} @ {self.center.name}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "program")
