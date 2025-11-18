from django.db.transaction import commit
from django.shortcuts import render,redirect
from django.template.context_processors import request
from django.views import View
from users.forms import RegistrationForm,TutorForm

from users.models import CustomUser
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

# Create your views here.

class HomeView(View):
    def get(self,request):
        return render(request,'index.html')

class LoginView(View):
    def get(self,request):
        return render(request,'registration\login.html')

    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if not user.is_active or not user.is_verified:
                messages.error(request, "Your account is not verified. Please check your email for OTP.")
                return redirect('users:login')
            login(request, user)
            return redirect('users:home')
        else:
            messages.error(request,'Invalid user credentials')
            return redirect('users:login')

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('users:login')

class RegistrationView(View):
    def get(self,request):
        form_instance=RegistrationForm()
        context={'form':form_instance}
        return render(request,'registration\signup.html',context)
    def post(self,request):
        form_instance=RegistrationForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)
            u.is_active=False
            u.save()
            u.generate_otp()
            send_mail(
                'OTP VERIFICATION',
                u.otp,
                "askcr31@gmail.com",
                [u.email],
                fail_silently=False
            )
            return redirect('users:otp')
        else:
            return render(request,'registration\signup.html',{'form':form_instance})

class OtpVerificationView(View):
    def post(self,request):
        o=request.POST.get('otp')
        try:
            u=CustomUser.objects.get(otp=o)
            u.is_verified=True
            u.is_active=True
            u.otp=None
            u.save()
            return redirect('users:login')
        except:
            messages.error(request,'Invalid OTP')
            return redirect('users:otp')

    def get(self,request):
        return render(request,'registration\otp.html')

class TutorJoinView(View):
    def get(self,request):
        form_instance=TutorForm()
        context={'form':form_instance}
        return render(request,'registration/tutorjoin.html',context)
    def post(self,request):
        u=request.user
        form_instance=TutorForm(request.POST,request.FILES)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            f.user=u
            u.is_tutor=True
            u.save()
            f.save()
        return redirect('users:home')