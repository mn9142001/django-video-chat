from django.urls import path

from .consumers import MeetingConsumer

websocket_urlpatterns = [
    path('video-meeting/<str:peerID>/', MeetingConsumer.as_asgi()),
]
