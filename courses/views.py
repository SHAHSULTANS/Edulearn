from time import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Course, Progress, Section, Lesson
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
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Course, Enrollment


class PublicCourseDetailView(DetailView):
    model = Course
    template_name = 'courses/public_course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = self.object  # get_object() result

        context['is_enrolled'] = False
        if user.is_authenticated:
            # Enrollment মডেল ব্যবহার করে চেক করা
            context['is_enrolled'] = Enrollment.objects.filter(student=user, course=course).exists()
        
        print(context["is_enrolled"])

        # একই ক্যাটাগরির রিলেটেড কোর্স তিনটি (নিজের কোর্স বাদ দিয়ে)
        context['related_courses'] = Course.objects.filter(
            category=course.category
        ).exclude(pk=course.pk)[:3]

        return context





class CourseLearningView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_learning.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        if not Enrollment.objects.filter(student=self.request.user, course=course).exists():
            messages.error(self.request, "You must be enrolled to access this course.")
            return redirect('courses:course_detail', pk=course.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user

        # Get all sections and lessons
        context['sections'] = course.sections.all()
        
        # Get progress for each lesson
        progress = Progress.objects.filter(student=user, lesson__section__course=course)
        context['progress'] = {p.lesson.id: p.completed for p in progress}

        # Calculate completion percentage
        total_lessons = sum(section.lessons.count() for section in course.sections.all())
        completed_lessons = progress.filter(completed=True).count()
        context['completion_percentage'] = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        # Get first accessible lesson (preview or enrolled)
        for section in course.sections.all():
            for lesson in section.lessons.all():
                if lesson.is_preview or Enrollment.objects.filter(student=user, course=course).exists():
                    context['current_lesson'] = lesson
                    break
            if 'current_lesson' in context:
                break

        return context

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        lesson_id = request.POST.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id, section__course=course)

        # Mark lesson as completed
        progress, created = Progress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'completed': True, 'completed_at': timezone.now()}
        )
        if not created and not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

        messages.success(request, f"Lesson '{lesson.title}' marked as completed!")
        return redirect('courses:course_learning', pk=course.pk)
    
    
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