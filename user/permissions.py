from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow full access for staff and read-only access for non-staff.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedStaff(permissions.BasePermission):
    """
    Custom permission to allow access only for authenticated staff members.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff