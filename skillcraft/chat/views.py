from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from users.models import Tutor

from chat.models import PrivateChatRoom
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from Tutor.models import Course

from chat.models import ChatMessage

from courses.models import Enroll


# Create your views here.


class ChatRoomView(LoginRequiredMixin,View):
    def get(self,request,tutor_id,course_id):
        tutor_profile=get_object_or_404(Tutor,id=tutor_id)
        tutor_user=tutor_profile.user
        student=request.user
        is_enrolled=Enroll.objects.filter(user=student,course=course_id).exists()
        if not is_enrolled:
            return HttpResponse("YOU MUST ENROLL IN THIS COURSE TO CHAT WITH TUTOR")
        room,created=PrivateChatRoom.objects.get_or_create(student=student,tutor=tutor_user)
        message=ChatMessage.objects.filter(room=room).order_by("timestamp")
        context={"room":room,"tutor":tutor_user,"student":student,"messages":message}
        return render(request,"chat/chat_room.html",context)



class TutorChatListView(LoginRequiredMixin, ListView):
    template_name = "chat/tutor_chat_list.html"
    context_object_name = "rooms"


    def get_queryset(self):
        return PrivateChatRoom.objects.filter(
            tutor=self.request.user
        ).select_related("student")




class TutorChatRoomView(LoginRequiredMixin,View):
    def get(self,request,pk):
        room=get_object_or_404(PrivateChatRoom,tutor=request.user,id=pk )
        student=room.student
        tutor=room.tutor
        message=ChatMessage.objects.filter(room=room).order_by('timestamp')
        context={'room':room,'student':student,'tutor':tutor,'messages':message}
        return render(request,"chat/chat_room.html",context)



