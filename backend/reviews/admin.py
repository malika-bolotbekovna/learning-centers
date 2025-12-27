from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "center", "author", "rating", "is_published", "created_at")
    list_filter = ("is_published", "rating")
    search_fields = ("center__title", "author__username")
