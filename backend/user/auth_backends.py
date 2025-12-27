from django.contrib.auth.backends import ModelBackend
from .models import Role

class RoleAdminBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj or not user_obj.is_authenticated:
            return False
        if getattr(user_obj, "role", None) == Role.ADMIN:
            return True
        return super().has_perm(user_obj, perm, obj=obj)

    def has_module_perms(self, user_obj, app_label):
        if not user_obj or not user_obj.is_authenticated:
            return False
        if getattr(user_obj, "role", None) == Role.ADMIN:
            return True
        return super().has_module_perms(user_obj, app_label)
