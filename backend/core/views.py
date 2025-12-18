from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Center, Program, Category, Favorite
from .serializers import CenterSerializer, ProgramSerializer, CategorySerializer, FavoriteSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProgramFilter

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

    ordering_fields = ["created_at", "price", "rating_avg"]
    ordering = ["-created_at"]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.none()  # важно для генерации схемы
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    # если используешь стандартный router — оставь pk по умолчанию

    def get_queryset(self):
        # Когда spectacular генерит схему — не дергаем БД и не трогаем request.user
        if getattr(self, "swagger_fake_view", False):
            return Favorite.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Favorite.objects.none()

        return (
            Favorite.objects
            .filter(user=user)  # важно: user=..., не user_id=self.request.user
            .select_related("program", "program__center", "program__category")
        )
    # при пост запросе юзера передаем не в теле запроса
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)