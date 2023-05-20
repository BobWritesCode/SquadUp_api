from rest_framework import permissions
from lfg.models import LFG
from lfg_slots.models import LFG_Slot


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


class IsGroupOwnerOrReadOnly(permissions.BasePermission):
    '''
    Permission class.

    Methods:
        has_object_permission - Checks to make sure the person reviewing an
        application is the group owner, otherwise read only.
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        slot = LFG_Slot.objects.get(pk=obj.slot.id)
        lfg = LFG.objects.get(pk=slot.lfg.id)
        return lfg.owner == request.user
