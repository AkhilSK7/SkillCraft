
from django.urls import path
from courses import views
app_name='courses'

urlpatterns = [
    path('<str:slug>',views.CategoryView.as_view(),name='category'),
    path('search/',views.SearchView.as_view(),name="search"),
    path('coursedetail/<int:pk>',views.CourseDetailView.as_view(),name="course"),
    path('video/<int:cid> <int:mid>', views.PlayvideoView.as_view(), name="video"),
    path('enroll/<int:id>',views.EnrollView.as_view(),name="enroll"),
    path('paymentsuccess/<str:i>',views.PaymentSuccessView.as_view(),name="complete"),
    path('enrolledcourses/',views.EnrolledCoursesView.as_view(),name="enrolledcourses")
]
