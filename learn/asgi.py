import os

from django.urls import path
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from learn.utils.consumers import CursorConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/cursor/", CursorConsumer.as_asgi()),
            ]
        )
    ),
})

app = application
