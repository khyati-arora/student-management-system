from rest_framework.permissions import BasePermission

class AdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == '3'

class StaffOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.user_type == '1' or request.user.user_type == '3')