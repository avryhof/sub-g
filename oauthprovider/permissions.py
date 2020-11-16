from rest_framework import permissions

from .models import AuthorizedAgent


class AuthorizedAgentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authorized = False

        try:
            AuthorizedAgent.objects.get(authorized=True, app_key=request.auth)

        except AuthorizedAgent.DoesNotExist:
            pass

        else:
            is_authorized = True

        return is_authorized


class AnonymousPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authorized = True

        return is_authorized
