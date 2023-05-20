from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Permission class.

    Methods:
        has_object_permission - Checks to make sure the person accessing an
        object is the owner, otherwise read only.
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
