from django.db import models
from django.conf import settings
from Tutor.models import Course
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Enroll(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="enrolled_courses")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="students")
    amount=models.IntegerField()
    is_enrolled=models.BooleanField(default=False)
    order_id=models.CharField(max_length=60,null=True)
    enrolled_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="reviews")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="reviews")
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],null=True)
    comments=models.TextField(max_length=80,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.course.course_name