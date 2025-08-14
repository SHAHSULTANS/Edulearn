from django.urls import path
from courses import views
from courses.views import (
    CourseCreateView, CourseDetailView, CourseEditView, CourseLearningView, PublicCourseDetailView, instructor_dashboard,
    section_create, SectionEditView, SectionDeleteView, LessonCreateView,
    LessonEditView, LessonDeleteView,manage_course
)

app_name = 'courses'

urlpatterns = [
    path('instructor-dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('pcourse/<int:pk>/', PublicCourseDetailView.as_view(), name='public_course_detail'),
    path('learning/<int:pk>/', CourseLearningView.as_view(), name='course_learning'),
    path('course/<int:pk>/edit/', CourseEditView.as_view(), name='course_edit'),
    path('course/<int:pk>/manage/', manage_course, name='manage_course'),
    path('course/<int:course_id>/section/create/', section_create, name='section_create'),
    path('course/<int:course_id>/section/<int:pk>/edit/', SectionEditView.as_view(), name='section_edit'),
    path('course/<int:course_id>/section/<int:pk>/delete/', SectionDeleteView.as_view(), name='section_delete'),
    path('course/<int:course_id>/section/<int:section_id>/lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('course/<int:course_id>/section/<int:section_id>/lesson/<int:pk>/edit/', LessonEditView.as_view(), name='lesson_edit'),
    path('course/<int:course_id>/section/<int:section_id>/lesson/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    
    
    path('enrolled-courses/', views.enrolled_course, name='enrolled_courses'),
]