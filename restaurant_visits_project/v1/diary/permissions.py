from rest_framework.permissions import BasePermission, IsAdminUser


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.pk == obj.creator_id
