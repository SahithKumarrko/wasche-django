from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import application.routing
application_r = ProtocolTypeRouter({
'websocket': AuthMiddlewareStack(
        URLRouter(
            application.routing.websocket_urlpatterns
        )
    ),
})