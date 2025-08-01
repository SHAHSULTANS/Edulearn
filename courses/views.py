from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Course, Section, Lesson
from .forms import CourseForm, SectionForm, LessonForm
from courses.models import Category


class InstructorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_instructor

class CourseCreateView(LoginRequiredMixin, InstructorRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:instructor_dashboard')

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Course created successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CourseEditView(LoginRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/edit_course.html'
    success_url = reverse_lazy('courses:instructor_dashboard')

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Course updated successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

#instructor details views
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
#single course detials views for all user

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Course

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Course

class PublicCourseDetailView(DetailView):
    model = Course
    template_name = 'courses/public_course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_enrolled'] = False
        if self.request.user.is_authenticated:
            context['is_enrolled'] = self.request.user.courses_enrolled.filter(pk=self.object.pk).exists()
        # Add related courses (same category, excluding current course)
        context['related_courses'] = Course.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context

def instructor_dashboard(request):
    if not request.user.is_instructor:
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    published_courses = courses.filter(is_published=True)
    return render(request, 'courses/instructor_dashboard.html', {
        'courses': courses,
        'published_courses': published_courses
    })


def manage_course(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    form = SectionForm(initial={'course': course})
    return render(request, 'courses/manage_course.html', {
        'course': course,
        'form': form
    })


def section_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id, instructor=request.user)
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, 'Section added successfully!')
            return redirect('courses:manage_course', pk=course.id)
    else:
        form = SectionForm(initial={'course': course})
    
    return render(request, 'courses/manage_course.html', {
        'form': form,
        'course': course
    })

class SectionEditView(LoginRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'courses/edit_section.html'

    def get_queryset(self):
        return Section.objects.filter(course__instructor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'], instructor=self.request.user)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Section updated successfully!')
        return redirect('courses:manage_course', pk=self.kwargs['course_id'])

class SectionDeleteView(LoginRequiredMixin, InstructorRequiredMixin, DeleteView):
    model = Section
    template_name = 'courses/manage_course.html'

    def get_queryset(self):
        return Section.objects.filter(course__instructor=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Section deleted successfully!')
        return reverse_lazy('courses:manage_course', kwargs={'pk': self.kwargs['course_id']})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

from django.urls import reverse

class LessonCreateView(LoginRequiredMixin, InstructorRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'], instructor=self.request.user)
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_id'], course__instructor=self.request.user)
        return context

    def form_valid(self, form):
        section = get_object_or_404(Section, pk=self.kwargs['section_id'], course__instructor=self.request.user)
        form.instance.section = section
        messages.success(self.request, 'Lesson added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:manage_course', kwargs={'pk': self.kwargs['course_id']})

from django.urls import reverse

class LessonEditView(LoginRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_form.html'

    def get_queryset(self):
        return Lesson.objects.filter(section__course__instructor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'], instructor=self.request.user)
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_id'], course__instructor=self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Lesson updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:manage_course', kwargs={'pk': self.kwargs['course_id']})

class LessonDeleteView(LoginRequiredMixin, InstructorRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'courses/manage_course.html'

    def get_queryset(self):
        return Lesson.objects.filter(section__course__instructor=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Lesson deleted successfully!')
        return reverse_lazy('courses:manage_course', kwargs={'pk': self.kwargs['course_id']})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)