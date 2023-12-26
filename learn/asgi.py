import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from learn.utils.consumers import CursorConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn.settings")


# http_application = get_asgi_application()


# websocket_router = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             [
#                 path("ws/cursor/", CursorConsumer.as_asgi()),
#             ]
#         )
#     ),
# })

# application = ProtocolTypeRouter({
#     "http": http_application,
#     "websocket": websocket_router,
# })

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
