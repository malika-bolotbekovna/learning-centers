import django_filters
from .models import Review

class ReviewFilter(django_filters.FilterSet):
    center = django_filters.NumberFilter(field_name="center__id")  # ?center=12

    class Meta:
        model = Review
        fields = ["center"]
