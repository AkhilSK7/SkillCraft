from django.forms import ModelForm
from courses.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['rating','comments']
