
from django.urls import path
from Tutor import views
app_name='tutor'

urlpatterns = [
    path('',views.TutorHomeView.as_view(),name='tutorhome'),
    path('uploadcourse',views.UploadCourseView.as_view(),name='uploadcourse'),
    path('tutorprofile',views.TutorProfileView.as_view(),name='tutorprofile'),
    path('edittutor',views.EditTutorView.as_view(),name='edittutor'),
path('uploadchapter',views.UploadChapterView.as_view(),name='uploadchapter'),
]
