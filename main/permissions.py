from rest_framework import permissions
from rest_framework.permissions import BasePermission


#читать всем, изменять только админу
class IsAdminOrReadOnly():
    def has_persmission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

