from rest_framework import permissions

ADMIN_ROLES = ('admin', 'moderator')


class isAdminOrReadOnly(metaclass=permissions.BasePermissionMetaclass):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated and
                (request.user.role == 'admin'
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return True


class isAdmin(metaclass=permissions.BasePermissionMetaclass):

    def has_permission(self, request, view):
        return (
                request.user.role == 'admin'
                or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return True

class isAdminOrMe(metaclass=permissions.BasePermissionMetaclass):
    # todo: user/me permissions
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True