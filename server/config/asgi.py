"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

from channels.routing               import ProtocolTypeRouter, URLRouter
from channels.auth                  import AuthMiddlewareStack
from channels.security.websocket    import AllowedHostsOriginValidator
from django.core.asgi               import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import prfl.routing
import chat.routing
# import game.routing
# import tournament.routing
from chat.middleware import TokenAuthenticationMiddleware

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                TokenAuthenticationMiddleware(
                    URLRouter( 
                        prfl.routing.websocket_urlpatterns + chat.routing.websocket_urlpatterns
                        # + game.routing.websocket_urlpatterns
                        # + tournament.routing.websocket_urlpatterns
                    )
                )
            )
        )
    }
)
