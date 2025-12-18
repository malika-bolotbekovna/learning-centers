from rest_framework import viewsets, permissions
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrAdminOrReadOnly
from core.models import Program

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("author", "program")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        review = serializer.save(author=self.request.user)
        avg = Review.objects.filter(program=review.program, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        Program.objects.filter(id=review.program_id).update(rating_avg=avg)

    def perform_update(self, serializer):
        review = serializer.save()
        avg = Review.objects.filter(program=review.program, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        Program.objects.filter(id=review.program_id).update(rating_avg=avg)

    def perform_destroy(self, instance):
        program = instance.program
        instance.delete()
        avg = Review.objects.filter(program=program, is_published=True).aggregate(a=Avg("rating"))['a'] or 0
        program.rating_avg = avg
        program.save(update_fields=["rating_avg"])
