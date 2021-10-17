from django.urls import re_path

from apps.chatroom import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
]
