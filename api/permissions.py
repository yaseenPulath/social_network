from rest_framework.permissions import BasePermission

class JWTPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user and request.user.id.__str__() == view.kwargs.get("pk", None):
            return True
        return False

        # return super().has_permission(request, view)