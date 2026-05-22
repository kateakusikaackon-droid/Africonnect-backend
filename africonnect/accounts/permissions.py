from rest_framework.permissions import BasePermission


#class RolePermission(BasePermission):

    #role = None

    #def has_permission(self, request, view):

        #return (
            #request.user.is_authenticated and
            #request.user.role == self.role
        #)

class RolePermission(BasePermission):

    role = None

    def has_permission(self, request, view):

        user = request.user

        return (
            user
            and user.is_authenticated
            and getattr(user, "role", None) == self.role
        )


class IsSupplier(RolePermission):
    role = "supplier"


class IsBuyer(RolePermission):
    role = "buyer"


class IsAdminUserRole(RolePermission):
    role = "admin"


class IsSupplierOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in ["supplier", "admin"]
        )


class IsBuyerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in ["buyer", "admin"]
        )
        