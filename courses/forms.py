

from django import forms
from .models import Course, Lesson,Student
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter course description', 'rows': 4}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in hours'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lesson title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lesson content', 'rows': 5}),
        }
        
        

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'enrolled_courses']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'enrolled_courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }