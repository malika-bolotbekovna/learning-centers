from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Center, Program, Category, Favorite
from .serializers import CenterSerializer, ProgramSerializer, CategorySerializer, FavoriteSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProgramFilter
from .pagination import SafePageNumberPagination

class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.filter(is_active=True)
    serializer_class = CenterSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "city", "address"]
    ordering_fields = ["name", "created_at"]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]


class ProgramViewSet(viewsets.ModelViewSet):
    pagination_class = SafePageNumberPagination
    queryset = Program.objects.select_related(
        "center", "category"
    ).filter(is_active=True)

    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ProgramFilter

    search_fields = [
        "title",
        "description",
        "topic",
        "center__name",
        "center__city",
    ]

    ordering_fields = ["created_at", "price"]
    ordering = ["-created_at"]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.none()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Favorite.objects.none()

        return (
            Favorite.objects
            .filter(user=self.request.user)
            .select_related("program", "program__center", "program__category")
        )

    def get_object(self):
        return get_object_or_404(
            Favorite,
            pk=self.kwargs["pk"],
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
