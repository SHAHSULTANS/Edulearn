from courses.models import Course
from django import forms
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'thumbnail', 
                  'level', 'requirements', 'what_you_will_learn']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'what_you_will_learn': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
