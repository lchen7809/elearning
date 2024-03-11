# """
# ASGI config for django_project project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """



import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from accounts.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

django_asgi_app = get_asgi_application()

import accounts.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)





# import os
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# # from django.urls import path
# # from accounts.consumers import ChatConsumer 
# import accounts.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             accounts.routing.websocket_urlpatterns  # Reference the websocket URL patterns
#         )
#     ),
# })


# import os
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import accounts.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# # application = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#                 accounts.routing.websocket_urlpatterns
#         )
#     ),
# })
