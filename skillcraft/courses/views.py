from django.shortcuts import render
from django.views.generic import ListView,DetailView
from Tutor.models import Course
from django.db.models import Q
# Create your views here.

class CategoryView(ListView):
    model=Course
    template_name='courses/courses.html'
    paginate_by = 10
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        return Course.objects.filter(category=slug)

class SearchView(ListView):
    model=Course
    template_name = 'courses/courses.html'
    paginate_by = 10
    def get_queryset(self):
        query=self.request.GET.get('q',"")
        if not query:
            return Course.objects.none()
        return Course.objects.filter(Q(course_name__icontains=query) | Q(description__icontains=query) |Q(category__icontains=query)|Q(Tutor__name__icontains=query))

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/coursedetail.html'
    context_object_name ="course"