
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.views import View
from Tutor.forms import CourseForm,ChapterForm,ModuleForm
from Tutor.models import Course,Chapter,Module
from users.models import Tutor
from users.forms import TutorForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class TutorAccessMixin(LoginRequiredMixin,UserPassesTestMixin):
    def dispatch(self, request, *args, **kwargs):
        self.t=Tutor.objects.get(user=kwargs['user_id'])
        return super().dispatch(request,*args,**kwargs)
    def test_func(self):
        return  self.request.user.is_tutor and self.t.user==self.request.user

# Create your views here.
class TutorHomeView(TutorAccessMixin,View):
    def get(self,request,user_id):
        c=Course.objects.filter(Tutor=self.t)
        context={'courses':c}
        return render(request,'tutor/tutorhome.html',context)


class TutorProfileView(TutorAccessMixin,View):
    def get(self,request,user_id):
        context={'tutor':self.t}
        return render(request,'tutor/tutorprofile.html',context)

class EditTutorView(TutorAccessMixin,View):
    def get(self,request,user_id):
        form_instance=TutorForm(instance=self.t)
        context={'form':form_instance}
        return render(request,'tutor/edittutorprofile.html',context)

    def post(self,request,user_id):
        form_instance=TutorForm(request.POST,request.FILES,instance=self.t)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('tutor:tutorprofile',user_id=user_id)

class ManageCourseView(TutorAccessMixin,View):
    def get(self,request,user_id,id):
        c=Course.objects.get(id=id)
        context={'course':c}
        return render(request,'tutor/manage_course.html',context)


class UploadCourseView(TutorAccessMixin,View):
    def get(self,request,user_id):
        form_instance=CourseForm()
        context={'form':form_instance}
        return render(request, 'tutor/uploadcourse.html',context)

    def post(self,request,user_id):
        form_instance=CourseForm(request.POST,request.FILES)
        if form_instance.is_valid():
            c=form_instance.save(commit=False)
            c.Tutor=self.t
            c.save()
            return redirect('tutor:managecourse',user_id=user_id,id=c.id)

class UploadChapterView(TutorAccessMixin,View):
    def get(self,request,user_id,id):
        form_instance=ChapterForm()
        context={'form':form_instance}
        return render(request,'tutor/uploadchapter.html',context)
    def post(self,request,user_id,id):
        form_instance=ChapterForm(request.POST)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            f.course=Course.objects.get(id=id)
            f.save()
            return redirect('tutor:managecourse',user_id=user_id,id=id)

class UploadModuleView(TutorAccessMixin,View):
    def get(self,request,user_id,id):
        form_instance=ModuleForm()
        context={'form':form_instance}
        return render(request,'tutor/uploadmodule.html',context)
    def post(self,request,user_id,id):
        form_instance=ModuleForm(request.POST,request.FILES)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            f.chapter=Chapter.objects.get(id=id)
            try:
                f.full_clean()
                f.save()
                return redirect('tutor:managecourse',user_id=user_id, id=id)
            except ValidationError as e:
                form_instance.add_error(None,e)

        return render(request, 'tutor/uploadmodule.html', {'form': form_instance})


class EditCourseView(TutorAccessMixin,View):
    def dispatch(self, request, *args, **kwargs):
        self.c=Course.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,user_id,id):
        form_instance=CourseForm(instance=self.c)
        context={'form':form_instance}
        return render(request,'tutor/uploadcourse.html',context)
    def post(self,request,user_id,id):
        form_instance=CourseForm(request.POST,request.FILES,instance=self.c)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('tutor:managecourse',user_id=user_id,id=self.c.id)




class EditChapterView(TutorAccessMixin,View):
    def dispatch(self, request, *args, **kwargs):
        self.c=Chapter.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,user_id,id):
        form_instance=ChapterForm(instance=self.c)
        context={'form':form_instance}
        return render(request,'tutor/uploadchapter.html',context)
    def post(self,request,user_id,id):
        form_instance=ChapterForm(request.POST,instance=self.c)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('tutor:managecourse',user_id=user_id, id=self.c.course.id)

        return render(request, 'tutor/uploadchapter.html', {'form': form_instance})

class DeleteChapterView(TutorAccessMixin,View):
    def get(self,request,user_id,id):
        c=Chapter.objects.get(id=id)
        c.delete()
        return redirect('tutor:managecourse',user_id=user_id, id=c.course.id)

class EditModuleView(TutorAccessMixin,View):
    def dispatch(self, request, *args, **kwargs):
        self.m=Module.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,user_id,id):
        form_instance=ModuleForm(instance=self.m)
        context={'form':form_instance}
        return render(request,'tutor/uploadmodule.html',context)
    def post(self,request,user_id,id):
        form_instance=ModuleForm(request.POST,request.FILES,instance=self.m)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            try:
                f.full_clean()
                f.save()
                return redirect('tutor:managecourse',user_id=user_id, id=self.m.chapter.course.id)
            except ValidationError as e:
                form_instance.add_error(None,e)
        return render(request, 'tutor/uploadmodule.html', {'form': form_instance})

class DeleteModuleView(TutorAccessMixin,View):
    def get(self,request,user_id,id):
        m=Module.objects.get(id=id)
        m.delete()
        return redirect('tutor:managecourse',user_id=user_id, id=m.chapter.course.id)


class TutorReviewsView(TutorAccessMixin,View):
    def get(self,request,user_id):
        courses=Course.objects.filter(Tutor=self.t).prefetch_related('reviews')
        context={'courses':courses}
        return render(request,'tutor/tutorreviews.html',context)