from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class PrivateChatRoom(models.Model):
    student=models.ForeignKey(User,related_name='student_rooms',on_delete=models.CASCADE)
    tutor=models.ForeignKey(User,related_name='tutor_rooms',on_delete=models.CASCADE,limit_choices_to={'is_tutor':True})
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("student","tutor")

    def __str__(self):
        return f"{self.student.username}<=>{self.tutor.username}"

class ChatMessage(models.Model):
    room=models.ForeignKey(PrivateChatRoom,related_name="messages",on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} : {self.message[:30]}"