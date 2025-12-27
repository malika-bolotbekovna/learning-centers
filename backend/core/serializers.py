from rest_framework import serializers
from .models import Center, Program, Category, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = (
            "id", "name", "description", "city", "address", "phone", "email",
            "website", "social_vk", "social_instagram", "social_telegram"
        )

class ProgramSerializer(serializers.ModelSerializer):
    center = CenterSerializer(read_only=True)
    center_id = serializers.PrimaryKeyRelatedField(source="center", queryset=Center.objects.all(), write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source="category", queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Program
        fields = (
            "id", "title", "description", "center", "center_id", "category", "category_id",
            "topic", "format", "price", "currency", "schedule",
            "age_min", "age_max", "is_active", "created_at"
        )

class FavoriteSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(source="program", queryset=Program.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "program", "program_id", "created_at")
