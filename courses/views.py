from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course
from django.contrib.auth.decorators import login_required

from courses.forms import CourseForm, SectionForm




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
    
    
def section_create(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SectionForm()
    return render(request, 'courses/section_form.html', {'form': form})



@login_required
def instructor_dashboard(request):
    if not request.user.is_instructor:
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_dashboard.html', {'courses': courses})