from django.urls import path

from .views import intent_responder

urlpatterns = [
    path("", intent_responder, name="subsonic-intent-responder"),
]
