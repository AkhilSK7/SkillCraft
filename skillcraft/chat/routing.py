from django.urls import path
from chat.consumers import PrivateChatConsumer

websocket_urlpatterns=[
    path('ws/chat/<int:room_id>/',PrivateChatConsumer.as_asgi()),
]