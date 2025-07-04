from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()





class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    requirements = models.TextField(blank=True)
    what_you_will_learn = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    
    

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
