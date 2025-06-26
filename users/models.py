

from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Category

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField('courses.Category', blank=True)
    # interests = models.ManyToManyField(blank=True,null=True)
    

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualifications = models.TextField()
    website = models.URLField(blank=True, null=True)