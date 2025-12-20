from django.contrib import admin
from chat.models import PrivateChatRoom,ChatMessage

# Register your models here.

admin.site.register(PrivateChatRoom)
admin.site.register(ChatMessage)