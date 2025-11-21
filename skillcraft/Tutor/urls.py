
from django.urls import path
from Tutor import views
app_name='tutor'

urlpatterns = [
    path('',views.TutorHomeView.as_view(),name='tutorhome'),
    path('uploadcourse',views.UploadCourseView.as_view(),name='uploadcourse'),
    path('tutorprofile',views.TutorProfileView.as_view(),name='tutorprofile'),
    path('edittutor',views.EditTutorView.as_view(),name='edittutor'),
path('uploadchapter/<int:id>',views.UploadChapterView.as_view(),name='uploadchapter'),
path('uploadmodule/<int:id>',views.UploadModuleView.as_view(),name='uploadmodule'),
path('managecourse/<int:id>',views.ManageCourseView.as_view(),name='managecourse'),
path('editchapter/<int:id>',views.EditChapterView.as_view(),name='editchapter'),
path('deletechapter/<int:id>',views.DeleteChapterView.as_view(),name='deletechapter'),
path('editmodule/<int:id>',views.EditModuleView.as_view(),name='editmodule'),
path('deletemodule/<int:id>',views.DeleteModuleView.as_view(),name='deletemodule'),
]
