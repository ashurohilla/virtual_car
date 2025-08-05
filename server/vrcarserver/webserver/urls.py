from django.urls import path, include
from channels.routing import URLRouter
from webserver.views import CarControlConsumer

urlpatterns = [
    path(r'^ws/car-control/$', CarControlConsumer.as_asgi()),
]