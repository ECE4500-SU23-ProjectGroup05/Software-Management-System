from django.urls import re_path
from MyServer.consumers import MyConsumer, WebConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', MyConsumer.as_asgi()),
    re_path(r'web-server', WebConsumer.as_asgi())
]
