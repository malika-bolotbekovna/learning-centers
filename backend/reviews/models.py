from django.db import models
from django.conf import settings
from core.models import Center

class Review(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("center", "author")

    def __str__(self):
        return f"{self.center.name} — {self.rating}★ by {self.author}"
