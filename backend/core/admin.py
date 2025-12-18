from django.contrib import admin
from .models import Center, Program, Category, Favorite

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "is_active")
    search_fields = ("name", "city")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "center", "format", "price", "rating_avg", "is_active")
    list_filter = ("format", "category")
    search_fields = ("title", "center__name")

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "program", "created_at")
