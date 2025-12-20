from django.urls import path
from chat import views

urlpatterns = [
    path("chatwith/<int:tutor_id>/",views.ChatRoomView.as_view(), name="chat_room"),
    path("tutor/chats/", views.TutorChatListView.as_view(), name="tutor_chat_list"),
    path("tutor/chat/<int:pk>/", views.TutorChatRoomView.as_view(), name="tutor_chat"),

]
