from rest_framework.permissions import BasePermission, SAFE_METHODS
from models import UserEmail

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)


# class IsValidatedOrReadOnly(BasePermission):
#     """
#     Custom permission, only users with at least one verified UserEmail can perform write operations on sections of courses of departments of faculties of institutions that there domain is associated with.
#     """
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return
#         try:
#             user_emails = UserEmail.objects.filer(user=request.user, is_verified=True)
