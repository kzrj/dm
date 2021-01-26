# # -*- coding: utf-8 -*-
from rest_framework import permissions


class SuggestionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff
        elif request.method == 'POST':
            return request.user
        elif request.method == 'PATCH':
            return request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff
        elif request.method == 'POST':
            return request.user.is_staff
        elif request.method == 'PATCH': 
            return request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False


class OwnerCUDPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return hasattr(request.user, 'profile')
        elif request.method == 'PATCH':
            return True
        elif request.method == 'DELETE':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user == obj.profile.user
        elif request.method == 'PATCH': 
            return request.user == obj.profile.user
        elif request.method == 'DELETE':
            return request.user == obj.profile.user
        return False