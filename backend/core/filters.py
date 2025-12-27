import django_filters as df
from .models import Program, ProgramFormat

class ProgramFilter(df.FilterSet):
    program_format = df.ChoiceFilter(field_name="format", choices=ProgramFormat.choices)
    center = df.NumberFilter(field_name="center__id")
    category = df.NumberFilter(field_name="category__id")  # ✅ добавили

    class Meta:
        model = Program
        fields = ["program_format", "center", "category"]   # ✅ добавили
