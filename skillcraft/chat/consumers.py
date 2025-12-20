import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from chat.models import PrivateChatRoom,ChatMessage

User=settings.AUTH_USER_MODEL

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id=self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name=f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            "type":"chat_message",
            "message":"Mention the course you are chatting about before starting chat",
            "sender": "Skillcraft",
        }))

    async def receive(self,text_data):
        data=json.loads(text_data)
        message=data['message']
        sender=self.scope["user"]
        
        room = await self.get_room(self.room_id)
        await self.save_message(room, sender, message)

        await self.channel_layer.group_send(self.room_group_name,{"type":"chat_message","message":message,"sender":sender.username,})

    async def chat_message(self,event):
        await self.send(text_data=json.dumps({"message":event["message"],"sender":event["sender"],}))
    @database_sync_to_async
    def get_room(self,room_id):
        return PrivateChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def save_message(self,room,sender,message):
        return ChatMessage.objects.create(room=room,sender=sender,message=message)


