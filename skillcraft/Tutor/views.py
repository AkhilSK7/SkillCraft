from django.shortcuts import render,redirect
from django.views import View
from Tutor.forms import CourseForm,ChapterForm,ModuleForm
from Tutor.models import Course
from users.models import Tutor
from users.forms import TutorForm

# Create your views here.
class TutorHomeView(View):
    def get(self,request):
        u=request.user
        t=Tutor.objects.get(user=u)
        c=Course.objects.filter(Tutor=t)
        context={'courses':c}
        return render(request,'tutor/tutorhome.html',context)


class UploadCourseView(View):
    def get(self,request):
        form_instance=CourseForm()
        context={'form':form_instance}
        return render(request, 'tutor/uploadcourse.html',context)

    def post(self,request):
        u=request.user
        t=Tutor.objects.get(user=u)
        form_instance=CourseForm(request.POST,request.FILES)
        if form_instance.is_valid():
            c=form_instance.save(commit=False)
            c.Tutor=t
            c.save()
            return redirect('tutor:tutorhome')


class TutorProfileView(View):
    def get(self,request):
        u=request.user
        t=Tutor.objects.get(user=u)
        context={'tutor':t}
        return render(request,'tutor/tutorprofile.html',context)

class EditTutorView(View):
    def get(self,request):
        u=request.user
        t=Tutor.objects.get(user=u)
        form_instance=TutorForm(instance=t)
        context={'form':form_instance}
        return render(request,'tutor/edittutorprofile.html',context)

    def post(self,request):
        u=request.user
        t = Tutor.objects.get(user=u)
        form_instance=TutorForm(request.POST,request.FILES,instance=t)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('tutor:tutorprofile')

class UploadChapterView(View):
    def get(self,request):
        form_instance=ChapterForm()
        context={'form':form_instance}
        return render(request,'tutor/uploadchapter.html',context)