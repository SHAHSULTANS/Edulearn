from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES)
        }