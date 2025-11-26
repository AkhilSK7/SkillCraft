
from django.urls import path
from courses import views
app_name='courses'

urlpatterns = [
    path('<str:slug>',views.CategoryView.as_view(),name='category'),
    path('search/',views.SearchView.as_view(),name="search"),
    path('coursedetail/<int:pk>',views.CourseDetailView.as_view(),name="course"),
]
