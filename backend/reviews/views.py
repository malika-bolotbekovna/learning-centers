from rest_framework import viewsets, permissions
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrAdminOrReadOnly
from core.models import Center
from .filters import ReviewFilter

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("author", "center")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    def perform_create(self, serializer):
        review = serializer.save(author=self.request.user)
        avg = Review.objects.filter(center=review.center, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        Center.objects.filter(id=review.center_id).update(rating_avg=avg)

    def perform_update(self, serializer):
        review = serializer.save()
        avg = Review.objects.filter(center=review.center, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        Center.objects.filter(id=review.center_id).update(rating_avg=avg)

    def perform_destroy(self, instance):
        center = instance.center
        instance.delete()
        avg = Review.objects.filter(center=center, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        center.rating_avg = avg
        center.save(update_fields=["rating_avg"])
