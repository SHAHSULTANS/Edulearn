from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User

# class Course(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     duration = models.IntegerField(help_text="Duration in hours")
#     thumbnail = models.ImageField(upload_to='course_thumbnail/', null=True, blank=True)
#     created_at = models.DateTimeField( default=timezone.now)

#     def __str__(self):
#         return self.title

# class Lesson(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     video_url = models.URLField(null=True, blank=True)
#     completion_status = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

# class Student(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="student")
#     name = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     enrolled_courses = models.ManyToManyField(Course, related_name='students', blank=True)
#     completed_lessons = models.ManyToManyField(Lesson, related_name='completed_by', blank=True)

#     def __str__(self):
#         return self.name
