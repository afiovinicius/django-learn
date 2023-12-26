import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from learn.utils.consumers import CursorConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn.settings")

application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/cursor/", CursorConsumer.as_asgi()),
            ]
        )
    ),
})


app = application
