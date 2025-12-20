from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from users.models import Tutor

from chat.models import PrivateChatRoom
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class ChatRoomView(LoginRequiredMixin,View):
    def get(self,request,tutor_id):
        tutor_profile=get_object_or_404(Tutor,id=tutor_id)
        tutor_user=tutor_profile.user
        student=request.user

        room, created=PrivateChatRoom.objects.get_or_create(student=student,tutor=tutor_user)
        context={"room":room,"tutor":tutor_profile}
        return render(request,"chat/chat_room.html",context)



class TutorChatListView(LoginRequiredMixin, ListView):
    template_name = "chat/tutor_chat_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return PrivateChatRoom.objects.filter(
            tutor=self.request.user
        ).select_related("student")


class TutorChatRoomView(LoginRequiredMixin, DetailView):
    model = PrivateChatRoom
    template_name = "chat/chat_room.html"
    context_object_name = "room"

    def get_queryset(self):
        # Security: tutor can only open their own rooms
        return PrivateChatRoom.objects.filter(
            tutor=self.request.user
        )

