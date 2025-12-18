from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CenterViewSet, ProgramViewSet, CategoryViewSet, FavoriteViewSet

router = DefaultRouter()
router.register("centers", CenterViewSet)
router.register("programs", ProgramViewSet)
router.register("categories", CategoryViewSet)
router.register("favorites", FavoriteViewSet, basename="favorites")

urlpatterns = [
    path("", include(router.urls)),
]
