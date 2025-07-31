from courses.models import Course, Lesson, Section
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



class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['course', 'title', 'order']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'duration', 'order', 'is_preview', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }