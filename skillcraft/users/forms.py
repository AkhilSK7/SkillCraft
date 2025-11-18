from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser,Tutor

class RegistrationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','password1','password2','email']


class TutorForm(forms.ModelForm):
    class Meta:
        model=Tutor
        fields=['name','description','profile_image']