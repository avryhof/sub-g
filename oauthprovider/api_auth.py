from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from .constants import API_AUTH_FAILED_RESPONSE_MESSAGE
from .models import AuthorizedAgent


class AssistantAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = None
        user = AnonymousUser()
        allowed_agents = list(AuthorizedAgent.objects.filter(authorized=True).values_list("app_key", flat=True))
        agent = request.META.get("HTTP_ASSISTANT_AGENT")

        if agent in allowed_agents:
            auth = agent
        else:
            raise AuthenticationFailed(detail=API_AUTH_FAILED_RESPONSE_MESSAGE)

        try:
            remote = AuthorizedAgent.objects.get(authorized=True, app_key=agent)
        except AuthorizedAgent.DoesNotExist:
            remote = None

        if remote:
            user = remote.user

        return (user, auth)


class AnonymousAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return (AnonymousUser, "")
