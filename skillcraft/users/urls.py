
from django.urls import path
from users import views
app_name='users'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('login',views.LoginView.as_view(),name='login'),
    path('signup',views.RegistrationView.as_view(),name='register'),
    path('otp',views.OtpVerificationView.as_view(),name='otp'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('TutorJoin',views.TutorJoinView.as_view(),name='tutorjoin'),
]
