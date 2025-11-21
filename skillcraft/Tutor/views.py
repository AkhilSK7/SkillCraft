from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.views import View
from Tutor.forms import CourseForm,ChapterForm,ModuleForm
from Tutor.models import Course,Chapter,Module
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
            return redirect('tutor:managecourse',id=c.id)


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
    def get(self,request,id):
        form_instance=ChapterForm()
        context={'form':form_instance}
        return render(request,'tutor/uploadchapter.html',context)
    def post(self,request,id):
        form_instance=ChapterForm(request.POST)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            f.course=Course.objects.get(id=id)
            return redirect('tutor:managecourse', id=id)

class UploadModuleView(View):
    def get(self,request,id):
        form_instance=ModuleForm()
        context={'form':form_instance}
        return render(request,'tutor/uploadmodule.html',context)
    def post(self,request,id):
        form_instance=ModuleForm(request.POST,request.FILES)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)

            f.chapter=Chapter.objects.get(id=id)
            try:
                f.full_clean()
                f.save()
                return redirect('tutor:managecourse', id=id)
            except ValidationError as e:
                form_instance.add_error(None,e)

        return render(request, 'tutor/uploadmodule.html', {'form': form_instance})


class ManageCourseView(View):
    def get(self,request,id):
        c=Course.objects.get(id=id)
        context={'course':c}
        return render(request,'tutor/manage_course.html',context)

class EditChapterView(View):
    def dispatch(self, request, *args, **kwargs):
        self.c=Chapter.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,id):
        form_instance=ChapterForm(instance=self.c)
        context={'form':form_instance}
        return render(request,'tutor/uploadchapter.html',context)
    def post(self,request,id):
        form_instance=ChapterForm(request.POST,instance=self.c)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('tutor:managecourse', id=self.c.course.id)

        return render(request, 'tutor/uploadchapter.html', {'form': form_instance})

class DeleteChapterView(View):
    def get(self,request,id):
        c=Chapter.objects.get(id=id)
        c.delete()
        return redirect('tutor:managecourse', id=c.course.id)

class EditModuleView(View):
    def dispatch(self, request, *args, **kwargs):
        self.m=Module.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,id):
        form_instance=ModuleForm(instance=self.m)
        context={'form':form_instance}
        return render(request,'tutor/uploadmodule.html',context)
    def post(self,request,id):
        form_instance=ModuleForm(request.POST,request.FILES,instance=self.m)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            try:
                f.full_clean()
                f.save()
                return redirect('tutor:managecourse', id=self.m.chapter.course.id)
            except ValidationError as e:
                form_instance.add_error(None,e)
        return render(request, 'tutor/uploadmodule.html', {'form': form_instance})

class DeleteModuleView(View):
    def get(self,request,id):
        m=Module.objects.get(id=id)
        m.delete()
        return redirect('tutor:managecourse', id=m.chapter.course.id)