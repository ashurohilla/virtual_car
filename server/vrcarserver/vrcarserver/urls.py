from django.urls import path
from django.contrib import admin
from channels.routing import ProtocolTypeRouter, URLRouter
from webserver.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # Other URL patterns for your Django app
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        urlpatterns
    ),
})