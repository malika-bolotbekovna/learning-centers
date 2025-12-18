from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        # только админ и автор может менять объект
        return bool(u and u.is_authenticated and (obj.author_id == u.id or getattr(u, "is_admin", False)))
