from django.conf import settings
from django.db import models
from django.db.models import DO_NOTHING


class AuthorizedAgent(models.Model):
    authorized = models.BooleanField(default=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        default=None,
        blank=True,
        null=True,
        on_delete=DO_NOTHING,
    )
    app_name = models.CharField(max_length=200, blank=True, null=True)
    app_key = models.TextField(blank=True, null=True)
