from django.db import models
from users.models import Tutor
from django.core.exceptions import ValidationError
# Create your models here.
class Course(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('finance', 'Finance & Accounting'),
        ('it_software', 'IT & Software'),
        ('office_productivity', 'Office Productivity'),
        ('personal_development', 'Personal Development'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('lifestyle', 'Lifestyle'),
        ('photography_video', 'Photography & Video'),
        ('health_fitness', 'Health & Fitness'),
        ('music', 'Music'),
        ('teaching_academics', 'Teaching & Academics'),
        ('unknown', "I don't know yet"),
    ]

    course_name=models.CharField(max_length=100)
    Tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
    category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    description=models.CharField(max_length=200)
    prerequisite=models.CharField(max_length=200)
    rating=models.DecimalField(max_digits=2,decimal_places=1,blank=True,null=True)
    review=models.CharField(max_length=300,blank=True,null=True)
    price=models.IntegerField()
    thumbnail=models.ImageField(upload_to='course_thumbnails')
    offer=models.IntegerField(null=True,blank=True)

class Chapter(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    chapter_name=models.CharField(max_length=30)


class Module(models.Model):
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE)
    module_name=models.CharField(max_length=30)
    video=models.FileField(upload_to='course_videos',blank=True,null=True)
    document=models.FileField(upload_to='course_documents',blank=True,null=True)

    def clean(self):
        if not self.video and not self.document:
            raise ValidationError("Please upload atleast one file:Video or Pdf")
