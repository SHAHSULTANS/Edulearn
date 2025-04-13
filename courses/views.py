from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

from courses.models import Course, Lesson, Student
from courses.forms import CourseForm, LessonForm, StudentForm, UserUpdateForm


def main_hompage(request):
    return render(request, "courses/index.html", {})


def home(request):
    courses = Course.objects.all()
    return render(request, "courses/home.html", {"courses": courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(user=request.user)
    student = students.first() if students.exists() else None

    total_lessons = course.lessons.count()
    completed_lessons = student.completed_lessons.filter(course=course).count() if student else 0
    progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

    context = {
        'course': course,
        'student': student,
        'progress': progress,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = Student.objects.filter(user=request.user).first()

    if student is None:
        messages.error(request, "No student profile found for this user!")
        return redirect('home')

    if lesson.course in student.enrolled_courses.all():
        student.completed_lessons.add(lesson)
        messages.success(request, f"Lesson '{lesson.title}' marked as complete!")
    else:
        messages.error(request, "You're not enrolled in this course!")

    return redirect('course_detail', course_id=lesson.course.id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def lesson_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {'form': form, 'course': course})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def lesson_update(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('course_detail', course_id=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {'form': form, 'lesson': lesson})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == "POST":
        course_id = lesson.course.id
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
        return redirect('course_detail', course_id=course_id)
    return render(request, 'courses/lesson_confirm_delete.html', {'lesson': lesson})


@login_required
def enroll_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            form.save_m2m()  # for many-to-many enrolled_courses
            messages.success(request, "Enrollment successful!")
            return render(request, 'courses/enrollment_success.html', {
                'student': student,
                'courses': student.enrolled_courses.all()
            })
    else:
        form = StudentForm()

    return render(request, 'courses/enroll_student.html', {'form': form})


@login_required
def view_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  # uses related_name="students" in Student model

    return render(request, 'courses/students_list.html', {
        'course': course,
        'students': students
    })


# Course management (accessible to any authenticated user, but can restrict later if needed)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully!")
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('home')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('home')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


# Authentication Views

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'courses/profile.html', {'form': form})




##_______________________________
#lab 9

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from django.contrib.auth.models import User
from .serializers import CourseSerializer

class CourseListAPI(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailAPI(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)





class EnrollStudentAPI(APIView):
    def post(self, request):
        try:
            # Get data from the request
            user_id = request.data.get('user')  # User ID
            name = request.data.get('name')     # Student's name
            email = request.data.get('email')   # Student's email
            course_id = request.data.get('course_id')  # Course ID

            # Ensure required fields are provided
            if not all([user_id, name, email, course_id]):
                return Response({'error': 'user, name, email, and course_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Try to get the course
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

            # Try to get the user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create or get the student
            student, created = Student.objects.get_or_create(
                email=email,  # Ensure that the email is unique
                defaults={'name': name, 'user': user}
            )

            # If the student already exists, we can optionally update the name if it's different
            if not created and student.name != name:
                student.name = name
                student.save()

            # Enroll the student in the course
            student.enrolled_courses.add(course)

            return Response({'message': f'{student.name} has been enrolled in {course.title}.'})

        except Exception as e:
            print("DEBUG ERROR:", e)
            return Response({'error': 'Something went wrong on the server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

