from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class SafePageNumberPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view=view)
        except NotFound:
            # Если page=1 и queryset пустой — возвращаем пустой список
            page = request.query_params.get(self.page_query_param, "1")
            if str(page) == "1" and not queryset.exists():
                self.request = request
                self.page = None
                return []
            # Если page не 1 — 404 логичен (страница реально не существует)
            raise

    def get_paginated_response(self, data):
        if self.page is None:
            return Response({"count": 0, "next": None, "previous": None, "results": data})
        return super().get_paginated_response(data)
