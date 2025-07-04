from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course

from courses.forms import CourseForm




class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

    def test_func(self):
        print("User:", self.request.user)
        print("Is instructor:", self.request.user.is_instructor)
        return self.request.user.is_instructor

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)