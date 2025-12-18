import django_filters as df
from .models import Program

class ProgramFilter(df.FilterSet):
    price = df.NumberFilter(field_name="price", lookup_expr="exact")
    format = df.CharFilter(field_name="format", lookup_expr="iexact")
    category = df.CharFilter(field_name="category__slug", lookup_expr="iexact")
    topic = df.CharFilter(field_name="topic", lookup_expr="icontains")
    city = df.CharFilter(field_name="center__city", lookup_expr="icontains")

    class Meta:
        model = Program
        fields = ["price", "format", "category", "topic", "city"]
