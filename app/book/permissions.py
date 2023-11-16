'''
customed permission for app
'''
from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    ''' Custom permission to only allow owner of an object to edit it'''

    def has_object_permission(self, request, view, obj):
        '''set object permission'''

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
