from rest_framework import permissions

ADMIN_MODERATOR_ROLES = ('admin', 'moderator')


class IsAdminOrReadOnly(metaclass=permissions.BasePermissionMetaclass):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser)
                )

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(metaclass=permissions.BasePermissionMetaclass):

    def has_permission(self, request, view):
        return (
                request.user.role == 'admin'
                or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsAdminOrModeratorOrMe(metaclass=permissions.BasePermissionMetaclass):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role in ADMIN_MODERATOR_ROLES
                     or request.user == obj.author)
        )
