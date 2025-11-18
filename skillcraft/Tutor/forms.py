from django.forms import Form,ModelForm
from Tutor.models import Course,Chapter,Module

class CourseForm(ModelForm):
    class Meta:
        model=Course
        fields=['course_name','category','description','prerequisite','price','thumbnail']


class ChapterForm(ModelForm):
    class Meta:
        model=Chapter
        fields='__all__'

class ModuleForm(ModelForm):
    class Meta:
        model=Module
        fields='__all__'

