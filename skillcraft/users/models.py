from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=6,blank=True,null=True)
    is_tutor=models.BooleanField(default=False)

    def generate_otp(self):
        self.otp= str(random.randint(100000,999999))
        self.save()

    def __str__(self):
        return self.username

class Tutor(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=200)
    profile_image=models.ImageField(upload_to='profileimages')

